# Stress Test Orchestrator - Detailed Methodology

This document contains the comprehensive stress testing methodology for the stress-test-orchestrator agent.

## Test Design Phases

### 1. Requirements Analysis & Target Identification
- **Clarify the target**: Identify exactly which functions, APIs, modules, or features to stress test
- **Understand the architecture**: Examine code structure, dependencies, data flows, and integration points
- **Define success criteria**: Establish performance baselines, acceptable response times, and throughput thresholds
- **Identify constraints**: Document resource limits, expected load patterns, and critical failure points

### 2. Stress Test Design

Design tests that progressively push the system beyond normal operating conditions:

- **Load Levels**: Define multiple test stages (normal load, peak load, stress load, breaking point)
- **Test Scenarios**: Create realistic use cases that mirror actual production traffic patterns
- **Concurrency Patterns**: Test with increasing numbers of simultaneous users/requests
- **Data Volume**: Include tests with large datasets, rapid data mutations, and data-intensive operations
- **Duration**: Include sustained load tests (30+ minutes) to identify memory leaks or resource exhaustion
- **Failure Injection**: Test behavior under resource constraints (CPU, memory, network limitations)

### 3. Technology Stack Detection & Tool Selection

**Detection Steps**:
1. Check `package.json` (Node.js)
2. Check `requirements.txt` or `pyproject.toml` (Python)
3. Check `pom.xml` or `build.gradle` (Java)
4. Check `go.mod` (Go)
5. Examine file extensions and imports

**Tool Selection by Stack**:

**Python Projects**:
- Use `locust`, `pytest-benchmark`, or custom threading/multiprocessing scripts
- Implement async/await patterns for concurrent operations
- Leverage `concurrent.futures` or `asyncio` for parallel execution

**JavaScript/Node.js Projects**:
- Use `artillery`, `k6`, or `loadtest` for API stress testing
- Implement worker threads for CPU-bound operations
- Utilize clustering for multi-process load generation

**Java Projects**:
- Use JMeter or Gatling for comprehensive load testing
- Implement JUnit performance tests with `@RepeatedTest`
- Leverage Java's concurrency utilities for parallel test execution

**Go Projects**:
- Implement goroutine-based concurrent testing
- Use `go test -count=N` and custom benchmark patterns
- Leverage channels for coordinating concurrent operations

### 4. Metrics Collection

**Performance Metrics**:
- Response times (min, max, mean, median, p95, p99)
- Throughput (requests/second, operations/second)
- Error rates and failure patterns
- Latency distribution and percentiles

**Resource Metrics**:
- CPU utilization percentages
- Memory consumption (heap, non-heap, garbage collection behavior)
- Network I/O bandwidth and connection counts
- Database connection pool usage
- Disk I/O rates

**Business Metrics** (when applicable):
- Transactions per second
- Conversion rates under load
- User journey completion rates

### 5. Test Execution Stages

1. **Baseline Test**: Establish normal performance characteristics
2. **Ramp-up Test**: Gradually increase load to find inflection points
3. **Stress Test**: Push system beyond expected capacity
4. **Sustained Load Test**: Maintain high load for extended periods
5. **Spike Test**: Simulate sudden traffic surges
6. **Recovery Test**: Verify system returns to normal after stress

During execution:
- Monitor system health and stop immediately if catastrophic failures occur
- Capture detailed logs at failure points
- Document any anomalies or unexpected behaviors
- Take snapshots at key load levels

### 6. Report Structure

**Executive Summary**:
- Overall assessment of system performance under stress
- Key findings and critical issues discovered
- Recommended actions and priority levels

**Detailed Results**:
- Performance metrics tables with comparisons across load levels
- Graphs showing response times, throughput, and error rates vs. load
- Resource utilization charts and timeline visualizations
- Identification of breaking points and failure modes

**Findings Analysis**:
- Bottleneck identification with specific code locations when possible
- Root cause analysis for performance degradation
- Comparison against defined success criteria
- Unexpected behaviors or anomalies observed

**Recommendations**:
- Specific code optimizations with implementation suggestions
- Infrastructure scaling recommendations (horizontal vs. vertical)
- Configuration tuning opportunities (caching, connection pools, timeouts)
- Architecture improvements for better resilience
- Priority ranking of issues by impact

## Quality Standards

- Tests must be reproducible with clear documentation
- All claims must be supported by data and evidence
- Reports must be actionable with specific recommendations
- Identify both critical and non-critical issues
- Highlight false positives and explain anomalous results
- Acknowledge test limitations and assumptions

## Edge Cases & Special Considerations

- Handle rate limiting and backpressure mechanisms appropriately
- Account for warm-up periods (JIT compilation, connection establishment)
- Consider external dependencies (third-party APIs, databases)
- Test both happy paths and error scenarios under stress
- Validate system behavior when resources are exhausted
- Test with realistic data distributions, not just uniform patterns
- Account for caching effects and design tests to measure cold vs. warm performance
