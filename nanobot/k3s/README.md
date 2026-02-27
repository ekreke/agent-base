# Nanobot k3s 部署指南

本文档描述如何将 Nanobot AI 服务部署到 k3s 集群。

## 目录结构

```
nanobot/
└── k3s/
    ├── deployment.yaml      # Deployment 配置
    ├── service.yaml         # Service 配置
    ├── kustomization.yaml   # Kustomize 配置
    └── README.md           # 本文档
```

## 快速部署

### 1. 构建 Docker 镜像

在 Nanobot 项目根目录执行：

```bash
cd /path/to/nanobot
docker build -t nanobot:latest .
```

### 2. 导入镜像到 k3s

**⚠️ 重要：k3s 使用 containerd，无法直接使用 Docker 的本地镜像**

```bash
# 将 Docker 镜像导入 k3s containerd
docker save nanobot:latest | sudo k3s ctr images import -

# 验证镜像已导入
sudo k3s ctr images ls | grep nanobot
# 应该看到: docker.io/library/nanobot:latest
```

### 3. 部署到 k3s

```bash
# 从 agent-base 目录部署
cd /path/to/agent-base/nanobot/k3s
kubectl apply -k .
```

### 4. 验证部署

```bash
# 查看 Pod 状态
kubectl get pods -l app=nanobot

# 查看 Service
kubectl get svc nanobot

# 获取访问地址
kubectl get nodes -o wide
# 服务通过 NodePort 30090 暴露
# 访问: http://<节点IP>:30090
```

### 5. 配置 API Key

Nanobot 需要配置 API key 才能正常工作：

```bash
# 创建配置目录（如果不存在）
mkdir -p ~/.nanobot

# 编辑配置
nano ~/.nanobot/config.json
```

配置文件格式：

```json
{
  "providers": {
    "openai": {
      "api_key": "your-api-key-here"
    }
  }
}
```

重启 Pod 使配置生效：

```bash
kubectl rollout restart deployment/nanobot
```

## 配置说明

### Deployment (deployment.yaml)

- **副本数**: 2 个 Pod
- **镜像**: docker.io/library/nanobot:latest
- **端口**: 18790
- **资源限制**:
  - CPU 限制: 1 核
  - 内存限制: 1Gi
  - CPU 请求: 250m
  - 内存请求: 256Mi
- **配置挂载**: `~/.nanobot` → `/root/.nanobot`

### Service (service.yaml)

- **类型**: NodePort
- **端口映射**: 18790 (容器) → 30090 (NodePort)
- **访问方式**: `http://<任意节点IP>:30090`

## 常用运维命令

```bash
# 查看日志
kubectl logs -l app=nanobot -f

# 扩缩容
kubectl scale deployment nanobot --replicas=3

# 更新部署
kubectl rollout restart deployment nanobot

# 查看部署状态
kubectl rollout status deployment/nanobot

# 进入 Pod 调试
kubectl exec -it <pod-name> -- /bin/bash

# 删除部署
kubectl delete -k .
```

---

## 部署问题排查

### 问题 1: HostPath 路径展开失败

**错误信息:**
```
MountVolume.SetUp failed for volume "config": hostPath type check failed: ~/.nanobot is not a directory
```

**原因:**
Kubernetes 不会展开 shell 路径中的 `~` 符号，`~/.nanobot` 被当作字面路径而非 `/home/ubuntu/.nanobot`。

**解决方案:**
1. 使用绝对路径
2. 使用 `DirectoryOrCreate` 类型自动创建目录

```yaml
volumes:
- name: config
  hostPath:
    path: /home/ubuntu/.nanobot  # 使用绝对路径
    type: DirectoryOrCreate       # 自动创建目录
```

### 问题 2: 镜像拉取失败 (ErrImageNeverPull)

**错误信息:**
```
Failed to pull image "nanobot:latest": rpc error: code = Unknown desc =
Error response from daemon: pull access denied for nanobot
```

**原因:**
- k3s 使用 containerd 作为容器运行时，与 Docker 是独立的
- `imagePullPolicy: Never` 要求镜像在本地存在
- Docker 构建的镜像在 containerd 中不可见

**解决方案:**
将 Docker 镜像导入 k3s containerd：

```bash
# 方法 1: 导入已有镜像
docker save nanobot:latest | sudo k3s ctr images import -

# 方法 2: 使用完整的镜像名称
# 修改 deployment.yaml 中的镜像名为: docker.io/library/nanobot:latest
```

**完整解决步骤:**

```bash
# 1. 使用 Docker 构建镜像
docker build -t nanobot:latest .

# 2. 导入到 k3s
docker save nanobot:latest | sudo k3s ctr images import -

# 3. 验证镜像
sudo k3s ctr images ls | grep nanobot
# 输出: docker.io/library/nanobot:latest

# 4. 确认 deployment.yaml 使用正确镜像名
image: docker.io/library/nanobot:latest
imagePullPolicy: Never

# 5. 重新部署
kubectl apply -k .
```

### 问题 3: 服务启动失败 - 缺少 API Key

**错误信息:**
```
Error: No API key configured.
Set one in ~/.nanobot/config.json under providers section
```

**解决方案:**
参见上文"配置 API Key"章节。

## 最佳实践总结

### 1. 镜像管理

对于本地开发/测试环境：

```bash
# 开发流程
docker build -t nanobot:latest .
docker save nanobot:latest | sudo k3s ctr images import -
kubectl rollout restart deployment/nanobot
```

对于生产环境，建议使用镜像仓库：

```yaml
# deployment.yaml
image: your-registry.com/nanobot:v1.0.0
imagePullPolicy: Always  # 或 IfNotPresent
```

### 2. 配置管理

- 使用 `DirectoryOrCreate` 避免手动创建目录
- 考虑使用 ConfigMap/Secret 管理敏感配置（生产环境）
- 本地开发可用 HostPath，生产环境建议用 PVC

### 3. 资源配置

根据实际负载调整资源限制：

```yaml
resources:
  limits:
    cpu: "2"      # 根据 CPU 密集型任务调整
    memory: 2Gi   # 根据模型大小和并发量调整
  requests:
    cpu: "500m"
    memory: 512Mi
```

### 4. 监控和日志

```bash
# 实时查看日志
kubectl logs -l app=nanobot -f --tail=100

# 查看所有 Pod 的日志（带前缀）
kubectl logs -l app=nanobot --prefix=true

# 查看事件
kubectl get events --sort-by='.lastTimestamp'
```

## 扩展部署

### 使用 Ingress 暴露服务

如果需要通过域名访问：

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: nanobot
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: websecure
spec:
  rules:
  - host: nanobot.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: nanobot
            port:
              number: 18790
```

### 使用 ConfigMap 管理配置

```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: nanobot-config
data:
  config.json: |
    {
      "providers": {
        "openai": {
          "api_key": "your-api-key"
        }
      }
    }
---
# deployment.yaml 更新
volumes:
- name: config
  configMap:
    name: nanobot-config
```
