import asyncio
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gmail_sync import sync_gmail
from task_service import get_tasks, complete_task


USER_ID = "test-user"


async def gmail_background_worker():
    """
    Automatically check Gmail for new messages.

    The Gmail history ID stored in Firestore ensures that
    only new messages are processed.
    """

    while True:
        try:
            print("\n[Background Worker] Checking Gmail...")

            result = sync_gmail(
                user_id=USER_ID,
            )

            print(
                f"[Background Worker] "
                f"messages_found={result['messages_found']} "
                f"tasks_created={result['tasks_created']}"
            )

        except Exception as e:
            print(f"[Background Worker] Error: {e}")

        await asyncio.sleep(60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Start the Gmail background worker when FastAPI starts.
    """

    worker = asyncio.create_task(
        gmail_background_worker()
    )

    print("[System] Gmail background worker started.")

    yield

    worker.cancel()

    try:
        await worker
    except asyncio.CancelledError:
        print("[System] Gmail background worker stopped.")


app = FastAPI(
    title="Personal Life Admin",
    description="AI-powered personal email task assistant",
    lifespan=lifespan,
)


@app.get("/", response_class=HTMLResponse)
def dashboard():
    """
    Serve the task dashboard.
    """

    return """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Personal Life Admin</title>

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;

    background: #f5f6f8;
    color: #171717;
}

.container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 40px 24px;
}

.header {
    margin-bottom: 30px;
}

.header h1 {
    margin: 0;
    font-size: 32px;
    font-weight: 700;
}

.header p {
    margin-top: 8px;
    color: #666;
    font-size: 15px;
}

.stats {
    display: grid;
    grid-template-columns:
        repeat(3, 1fr);

    gap: 16px;

    margin-bottom: 32px;
}

.stat {
    background: white;
    border-radius: 14px;
    padding: 20px;

    border: 1px solid #e5e5e5;
}

.stat-number {
    font-size: 28px;
    font-weight: 700;
}

.stat-label {
    margin-top: 5px;
    color: #777;
    font-size: 14px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    margin-bottom: 14px;
}

.section-header h2 {
    margin: 0;
    font-size: 20px;
}

.refresh {
    color: #666;
    font-size: 13px;
}

.task {
    background: white;

    border: 1px solid #e5e5e5;
    border-radius: 14px;

    padding: 20px;

    margin-bottom: 12px;

    display: flex;
    justify-content: space-between;
    gap: 20px;

    transition: 0.15s ease;
}

.task:hover {
    border-color: #cfcfcf;
}

.task-main {
    flex: 1;
}

.task-title {
    font-size: 17px;
    font-weight: 650;

    margin-bottom: 8px;
}

.task-description {
    color: #666;
    font-size: 14px;
    line-height: 1.5;

    margin-bottom: 14px;
}

.metadata {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.badge {
    display: inline-block;

    padding: 5px 9px;

    border-radius: 7px;

    background: #f0f1f3;

    font-size: 12px;
    color: #555;
}

.priority-high {
    background: #fff0f0;
    color: #b42318;
}

.priority-medium {
    background: #fff8e6;
    color: #946200;
}

.priority-low {
    background: #eef8f1;
    color: #267344;
}

.complete-button {
    align-self: center;

    border: 0;
    border-radius: 9px;

    padding: 10px 15px;

    background: #171717;
    color: white;

    font-size: 13px;
    font-weight: 600;

    cursor: pointer;
}

.complete-button:hover {
    opacity: 0.8;
}

.completed-section {
    margin-top: 40px;
}

.completed-task {
    opacity: 0.55;
}

.completed-task .task-title {
    text-decoration: line-through;
}

.empty {
    background: white;

    border: 1px dashed #d5d5d5;
    border-radius: 14px;

    padding: 35px;

    text-align: center;

    color: #777;
}

@media (max-width: 700px) {

    .stats {
        grid-template-columns: 1fr;
    }

    .task {
        flex-direction: column;
    }

    .complete-button {
        align-self: flex-start;
    }

}

</style>

</head>


<body>

<div class="container">

    <div class="header">

        <h1>Personal Life Admin</h1>

        <p>
            AI-powered task management from your Gmail inbox
        </p>

    </div>


    <div class="stats">

        <div class="stat">

            <div
                class="stat-number"
                id="active-count">
                -
            </div>

            <div class="stat-label">
                Active tasks
            </div>

        </div>


        <div class="stat">

            <div
                class="stat-number"
                id="high-count">
                -
            </div>

            <div class="stat-label">
                High priority
            </div>

        </div>


        <div class="stat">

            <div
                class="stat-number"
                id="completed-count">
                -
            </div>

            <div class="stat-label">
                Completed
            </div>

        </div>

    </div>


    <div class="section-header">

        <h2>Active Tasks</h2>

        <div
            class="refresh"
            id="last-updated">
            Loading...
        </div>

    </div>


    <div id="active-tasks"></div>


    <div class="completed-section">

        <div class="section-header">

            <h2>Completed</h2>

        </div>

        <div id="completed-tasks"></div>

    </div>

</div>


<script>

async function loadTasks() {

    try {

        const response =
            await fetch("/tasks");

        const tasks =
            await response.json();


        const active =
            tasks.filter(
                task =>
                    task.status !== "completed"
            );


        const completed =
            tasks.filter(
                task =>
                    task.status === "completed"
            );


        document.getElementById(
            "active-count"
        ).textContent = active.length;


        document.getElementById(
            "completed-count"
        ).textContent = completed.length;


        document.getElementById(
            "high-count"
        ).textContent =
            active.filter(
                task =>
                    task.priority === "high"
            ).length;


        renderTasks(
            active,
            "active-tasks",
            false
        );


        renderTasks(
            completed,
            "completed-tasks",
            true
        );


        document.getElementById(
            "last-updated"
        ).textContent =
            "Updated " +
            new Date().toLocaleTimeString();

    }

    catch (error) {

        console.error(
            "Failed to load tasks:",
            error
        );

    }

}


function renderTasks(
    tasks,
    elementId,
    isCompleted
) {

    const container =
        document.getElementById(elementId);


    if (tasks.length === 0) {

        container.innerHTML =
            `<div class="empty">
                No tasks here.
            </div>`;

        return;
    }


    container.innerHTML =
        tasks.map(task => {

            const priority =
                task.priority || "medium";

            const priorityClass =
                "priority-" + priority;


            const deadline =
                task.deadline
                    ? "Due: " + task.deadline
                    : "No deadline";


            const category =
                task.category || "General";


            const confidence =
                task.confidence !== undefined
                    ? Math.round(
                        task.confidence * 100
                    ) + "% confidence"
                    : "";


            return `

                <div class="task
                    ${isCompleted
                        ? "completed-task"
                        : ""}">

                    <div class="task-main">

                        <div class="task-title">
                            ${escapeHtml(
                                task.title
                            )}
                        </div>


                        <div class="task-description">
                            ${escapeHtml(
                                task.description || ""
                            )}
                        </div>


                        <div class="metadata">

                            <span class="badge">
                                ${escapeHtml(
                                    category
                                )}
                            </span>


                            <span class="badge">
                                ${escapeHtml(
                                    deadline
                                )}
                            </span>


                            <span
                                class="badge
                                    ${priorityClass}">
                                ${escapeHtml(
                                    priority
                                )}
                            </span>


                            <span class="badge">
                                ${escapeHtml(
                                    confidence
                                )}
                            </span>

                        </div>

                    </div>


                    ${
                        !isCompleted
                            ? `
                                <button
                                    class="complete-button"
                                    onclick=
                                    "completeTask(
                                        '${task.id}'
                                    )">

                                    Complete

                                </button>
                              `
                            : ""
                    }

                </div>

            `;

        }).join("");

}


async function completeTask(taskId) {

    try {

        const response =
            await fetch(
                "/tasks/" +
                taskId +
                "/complete",
                {
                    method: "POST"
                }
            );


        if (!response.ok) {

            throw new Error(
                "Failed to complete task"
            );

        }


        await loadTasks();

    }

    catch (error) {

        console.error(error);

        alert(
            "Could not complete the task."
        );

    }

}


function escapeHtml(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value;

    return div.innerHTML;

}


loadTasks();


// Automatically refresh the dashboard
// every 15 seconds.

setInterval(
    loadTasks,
    15000
);

</script>

</body>

</html>
"""


@app.get("/tasks")
def tasks():
    """
    Return all tasks as JSON.
    """

    return get_tasks(
        user_id=USER_ID,
    )


@app.post("/tasks/{task_id}/complete")
def complete(task_id: str):
    """
    Mark a task as completed.
    """

    result = complete_task(
        user_id=USER_ID,
        task_id=task_id,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {
        "status": "completed",
        "task_id": task_id,
    }


@app.post("/sync")
def sync():
    """
    Manually trigger a Gmail sync.

    The background worker normally handles this automatically.
    """

    return sync_gmail(
        user_id=USER_ID,
    )