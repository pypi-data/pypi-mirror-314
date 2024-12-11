from mhagenta.gui.monitor import Monitor
import asyncio


TEST_LOGS = [
    '===== BUILDING RABBITMQ BASE IMAGE: mha-rabbitmq:1.1.1 =====',
    '===== BUILDING AGENT BASE IMAGE: mha-base:1.1.1 =====',
    '===== BUILDING AGENT IMAGE: mhagent:test_agent =====',
    '===== RUNNING AGENT IMAGE \"mhagent:test_agent\" AS CONTAINER \"test_agent\" =====',
    'Using MHAgentA version 1.0.12a2',
    '[0.005500|0.005500|-][WARNING]::[test_agent][root][RootMessenger][RabbitMQConnector]::Opening connection failed: ! Retrying...',
    '[1.006900|1.006800|-][WARNING]::[test_agent][root][RootMessenger][RabbitMQConnector]::Opening connection failed: ! Retrying...',
    '[5.069600|5.069600|-][CRITICAL]::[test_agent][root]::[status_upd]::perceptor:DECLARED,actuator:DECLARED,ll_reasoner:DECLARED,knowledge:DECLARED,hl_reasoner:DECLARED,goal_graph:DECLARED',
    '[7.343500|2.016500|-][INFO]::[test_agent][goal_graph]::Received start command (start ts: 7.34486985206604)',
    '[7.343700|2.038800|-][INFO]::[test_agent][perceptor]::Received start command (start ts: 7.34486985206604)',
    '[7.343700|2.034900|-][INFO]::[test_agent][hl_reasoner]::Received start command (start ts: 7.34486985206604)',
    '[7.343800|2.057600|-][INFO]::[test_agent][knowledge]::Received start command (start ts: 7.34486985206604)',
    '[7.343800|2.051000|-][INFO]::[test_agent][ll_reasoner]::Received start command (start ts: 7.34486985206604)',
    '[7.343800|2.029700|-][INFO]::[test_agent][actuator]::Received start command (start ts: 7.34486985206604)',
    '[7.346300|2.041500|0.0015][INFO]::[test_agent][perceptor]::Received observation request c7c8986ad2f4 from ll_reasoner. Processing...',
    '[7.351400|2.046500|0.0065][WARNING]::[test_agent][perceptor]::Caught exception \"HTTPConnectionPool(host=\'host.docker.internal\', port=8000): Max retries exceeded with url: /observation (Caused by NewConnectionError(\'<urllib3.connection.HTTPConnection object at 0x7fd52f7e1d00>: Failed to establish a new connection: [Errno 111] Connection refused\'))\" while processing message c7c8986ad2f4 from ll_reasoner (channel: ll_reasoner_perceptor_request)! Aborting message processing and attempting to resume execution...',
    '[7.569600|7.569600|0.2248][CRITICAL]::[test_agent][root]::[status_upd]::perceptor:RUNNING,actuator:READY,ll_reasoner:READY,knowledge:READY,hl_reasoner:READY,goal_graph:READY',
    '[10.069600|10.069500|2.7247][CRITICAL]::[test_agent][root]::[status_upd]::perceptor:RUNNING,actuator:READY,ll_reasoner:READY,knowledge:READY,hl_reasoner:READY,goal_graph:READY',
    '[12.569600|12.569600|5.2247][CRITICAL]::[test_agent][root]::[status_upd]::perceptor:RUNNING,actuator:RUNNING,ll_reasoner:RUNNING,knowledge:RUNNING,hl_reasoner:RUNNING,goal_graph:RUNNING',
    '[15.069600|15.069600|7.7247][CRITICAL]::[test_agent][root]::[status_upd]::perceptor:RUNNING,actuator:RUNNING,ll_reasoner:RUNNING,knowledge:RUNNING,hl_reasoner:RUNNING,goal_graph:RUNNING',
    '[17.344900|17.344800|10.0][INFO]::[test_agent][root]::Stopping! Reason: TIMEOUT.',
    '[17.345000|17.345000|10.0002][INFO]::[test_agent][root]::Sending stop command (reason AGENT TIMEOUT CMD)',
    '[17.344900|12.040000|10.0][INFO]::[test_agent][perceptor]::Stopping! Reason: TIMEOUT.',
    '[17.344900|12.052100|10.0][INFO]::[test_agent][ll_reasoner]::Stopping! Reason: TIMEOUT.',
    '[17.344900|12.036100|10.0][INFO]::[test_agent][hl_reasoner]::Stopping! Reason: TIMEOUT.',
    '[17.344900|12.030700|10.0][INFO]::[test_agent][actuator]::Stopping! Reason: TIMEOUT.',
    '[17.344900|12.058800|10.0][INFO]::[test_agent][knowledge]::Stopping! Reason: TIMEOUT.',
    '[17.345000|12.052200|10.0001][INFO]::[test_agent][ll_reasoner]::Stopping',
    '[17.344900|12.017900|10.0][INFO]::[test_agent][goal_graph]::Stopping! Reason: TIMEOUT.',
    '[17.345000|12.040100|10.0001][INFO]::[test_agent][perceptor]::Stopping',
    '[17.345000|12.036200|10.0001][INFO]::[test_agent][hl_reasoner]::Stopping',
    '[17.345000|12.030800|10.0001][INFO]::[test_agent][actuator]::Stopping',
    '[17.345000|12.058900|10.0001][INFO]::[test_agent][knowledge]::Stopping',
    '[17.345000|12.018000|10.0002][INFO]::[test_agent][goal_graph]::Stopping',
    '[19.368800|14.063900|12.0239][INFO]::[test_agent][perceptor]::Stopped!',
    'Module perceptor exited, reason: TIMEOUT',
    '[20.365500|15.051400|13.0207][INFO]::[test_agent][actuator]::Stopped!',
    'Module actuator exited, reason: TIMEOUT',
    '[20.372900|15.064100|13.0281][INFO]::[test_agent][hl_reasoner]::Stopped!',
    'Module hl_reasoner exited, reason: TIMEOUT',
    '[21.369800|16.042800|14.0249][INFO]::[test_agent][goal_graph]::Stopped!',
    '[21.371500|16.078800|14.0267][INFO]::[test_agent][ll_reasoner]::Stopped!',
    'Module goal_graph exited, reason: TIMEOUT',
    'Module ll_reasoner exited, reason: TIMEOUT',
    '[21.377600|16.091400|14.0327][INFO]::[test_agent][knowledge]::Stopped!',
    'Module knowledge exited, reason: TIMEOUT',
    '[22.420700|22.420700|15.0759][INFO]::[test_agent][root]::Stopped!',
    'Shutting down RabbitMQ node rabbit@6de6621e7635 running at PID 24',
    'Waiting for PID 24 to terminate',
    'RabbitMQ node rabbit@6de6621e7635 running at PID 24 successfully shut down',
    '===== EXECUTION FINISHED ====='
]


async def test():
    monitor = Monitor(auto_select_new=False)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(monitor.run())
        await asyncio.sleep(1)
        monitor.add_agent('test_agent', ['root', 'actuator', 'perceptor', 'll_reasoner',
                                          'hl_reasoner', 'knowledge', 'goal_graph'])
        monitor.add_agent('test_agent2', ['root', 'actuator', 'perceptor', 'll_reasoner',
                                          'hl_reasoner', 'knowledge', 'goal_graph'])
        # monitor.add_agent('test_agent2', ['root', 'mod3', 'mod4'])

        await asyncio.sleep(1)
        for log in TEST_LOGS:
            monitor.add_log(log)
            await asyncio.sleep(0.5)


# async def task1(monitor: Monitor):


if __name__ == '__main__':
    asyncio.run(test())
