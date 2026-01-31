# Design a data pipeline to load data from an API into a data warehouse
# How would you identify and fix data discrepancies in a pipeline?
# Explain how you would scale a pipeline to handle a sudden increase in data volume
- using a distributed processing framework or multiple workers/containers so that more compute nodes can be added when volume spikes. Instead of one big job on one machine, the work is split into many smaller tasks that can run in parallel.
- the pipeline should be designed to process data incrementally rather than reprocessing everything from scratch. If only new or changed data is processed (for example via batching, windowing, or change data capture), a spike in input size only increases the size or number of new batches, not the total historical workload.
- decouple ingestion from processing using a buffer or queue (such as a message queue or log system). This absorbs bursts of incoming data and allows downstream processing to catch up at its own pace. Backpressure mechanisms or rate limits prevent the system from being overwhelmed.
- ensure data is partitioned so work can be evenly distributed. Good partitioning keys (like date, region, or ID ranges) allow different workers to operate independently on separate slices of the data, avoiding hotspots where one worker does most of the work.
- for heavy operations like joins and aggregations, use strategies that reduce data movement, such as pre-aggregating, filtering early, and colocating related data where possible. This minimises expensive shuffling or network transfer when volumes grow.
- autoscaling is also important. The compute layer should be able to automatically add more workers when queues grow or processing lag increases, and scale back down when load returns to normal. This provides elasticity without permanent overprovisioning.
- on the storage side, optimise file or data layout to keep reads efficient at larger scale. Avoid huge single files and also avoid millions of tiny files; aim for moderately sized chunks so many workers can read in parallel.
- continuously monitor throughput, latency, queue depth, error rates, and resource utilisation. Scaling decisions should be driven by these metrics. If processing time per batch starts exceeding the arrival rate, add parallelism or resources; if resources are underutilised, scale down.
# Describe a situation where you had to troubleshoot a failed data pipeline
# How would you implement a fault tolerant system for data ingestion
To implement a fault tolerant data ingestion system, the goal is to make sure that temporary failures, retries, or restarts do not cause data loss, duplication, or corruption.

The first principle is durability of the raw input. Incoming data should land in a reliable, persistent store (for example object storage or a durable message log) before any heavy processing happens. This creates a replayable source of truth so if downstream processing fails, you can reprocess the same input again.

Next, ingestion should be idempotent. If the same batch or event is processed twice due to a retry, the end result should still be correct. This can be achieved using unique identifiers, upserts/merges instead of blind inserts, or deduplication logic based on keys and timestamps.

Checkpointing is another key piece. The ingestion job should regularly record its progress (for example last processed offset, file, or timestamp) in durable storage. On restart, the job reads this checkpoint and continues from that exact point instead of starting over or skipping data.

Retries should be automatic and safe. Transient failures like network timeouts should trigger retries with exponential backoff, but because of idempotency and checkpoints, those retries won’t create duplicates.

To handle bursts and temporary downstream outages, introduce a buffer layer such as a queue or log. This decouples producers from consumers. Producers can continue writing data even if the ingestion processor is temporarily down, and the consumer can catch up later from the buffered backlog.

The system should also write data atomically. Each ingestion unit (for example a batch) should either fully succeed or have no visible effect. Using transactional or atomic writes prevents partially written data from appearing in the target if a failure occurs mid-write.

Validation and quarantine paths help protect data quality. If some records are malformed, they should be diverted to a dead-letter or quarantine store instead of crashing the whole pipeline. This allows ingestion to continue for good data while bad data is inspected separately.

Monitoring and alerting close the loop. Track lag, failure counts, retry rates, and throughput. If lag grows or retries exceed a threshold, trigger alerts or autoscaling so the system can recover before data loss or long delays occur.