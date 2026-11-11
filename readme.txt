连续健康随访采集调度器
慢病与术后随访团队按队列和节律生成本地联络计划，验证问卷时序一致性，对失访和恶化信号创建人工任务。

测试：python3 -m unittest discover -s tests/followup_scheduler -p 'test_*.py'
构建：python3 -m compileall -q continuity_coordinator tests/followup_scheduler
验收：python3 -m continuity_coordinator.operations.followup_cli --fixture fixtures/demo.json --database /tmp/followup_scheduler-acceptance.sqlite3
