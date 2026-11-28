
type ProjectModalProps = {
    onClose: () => void
    year: number
    month: number
    startDate: number
    endDate: number
}

function ProjectModal({
    onClose,
    year,
    month,
    startDate,
    endDate
}: ProjectModalProps) {

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h2>Create Project</h2>

                <div>
                    <label>Project Name</label>
                    <input
                        type="text"
                        placeholder="Enter project name"
                    />
                </div>

                <div>
                    <label>Description</label>
                    <textarea
                        placeholder="Enter project description"
                    />
                </div>

                <div>
                    <p>Start Date: {year}-{month + 1}-{startDate}</p>
                    <p>End Date: {year}-{month + 1}-{endDate}</p>
                </div>

                <div>
                    <button>
                        Invite Members
                    </button>
                </div>

                <button onClick={onClose}>
                    Cancel
                </button>
            </div>
        </div>
    )
}

export default ProjectModal
