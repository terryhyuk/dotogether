
function Calendar() {

    const today = new Date()
    const year = today.getFullYear()
    const month = today.getMonth()
    const date = today.getDate()

    // Get the first day of the current month
    const firstDay = new Date(year, month, 1).getDay()

    // Generate empty spaces before the first date
    const blanks = Array.from(
        { length: firstDay },
        (value, index) => index
    )

    // Get the last date of the current month
    const lastDate = new Date(year, month + 1, 0).getDate()

    // Generate an array of dates
    const dates = Array.from(
        { length: lastDate },
        (value, index) => index + 1
    )

    return (
        <div>
            <h1>DoTogether Calendar</h1>

            <div>
                <button>Previous</button>
                <h2>{year}년 {month + 1}월</h2>
                <button>Next</button>
            </div>

            {/* Weekdays */}
            <div className="calendar-grid">
                {["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"].map(day => (
                    <div key={day}>
                        {day}
                    </div>
                ))}
            </div>

            {/* Calendar dates */}
            <div className="calendar-grid">
                {blanks.map(blank => (
                    <div key={`blank-${blank}`}></div>
                ))}

                {dates.map(day => (
                    <div
                        key={day}
                        className={day === date ? 'today' : ''}
                    >
                        {day}
                    </div>
                ))}
            </div>
        </div>
    )
}

export default Calendar
