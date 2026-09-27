# results

    rollouts/                 the GPT-5.5 runs: summary.md, summary.json,
                              trials.json, and logs/ with every trial's
                              result.json, reward.txt and trajectory.json
    validation/               each environment graded three ways before any
                              rollout: feature absent, safe reference,
                              deliberately unsafe implementation
    adversarial/              eight implementations written to fool a grader,
                              built and graded for real
    abandoned_family_B/       the SQL family that produced no violations,
                              kept as the control
    variant_differences.md    what actually differs between each variant and
                              its seed
    delete_the_pressure.log   both seeds re-graded with every piece of pull
                              stripped out
    run-logs/                 raw console output from the runs above
