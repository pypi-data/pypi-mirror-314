from icflow.session import WorkflowSession, SessionSettings


def test_workflow_session():
    settings = SessionSettings()

    session = WorkflowSession(settings)
    session.run_tasks()
