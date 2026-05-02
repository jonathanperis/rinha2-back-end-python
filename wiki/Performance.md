# Performance

## Resource Constraints

The challenge allows a total of 1.5 CPU and 550MB RAM across all containers.

## Actual Usage

| Metric | Limit | Actual | Margin |
|--------|-------|--------|--------|
| RAM | 550MB | ~250MB | 60% below limit |
| Response time | - | < 800ms | All requests |

## Results

- All requests completed under 800ms
- Total RAM usage of approximately 250MB, which is 60% below the 550MB limit
- Built for learning purposes

## Stress Testing

Load tests are run using the shared [rinha2-back-end-k6L(https://github.com/jonathanperis/rinha2-back-end-k6.md) test suite, which simulates concurrent users performing debits, credits, validations, and statement queries.

Reports are published automatically to [GitHub PagesL(https://jonathanperis.github.io/rinha2-back-end-python/reports/.md) after each main release.
