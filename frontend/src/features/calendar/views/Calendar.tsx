import { useState, useEffect, useRef } from "react"
import ProjectModal from "../components/ProjectModal"

function Calendar() {

    const today = new Date()
    const calendarRef = useRef<HTMLDivElement>(null)

    const [currentDate, setCurrentDate] = useState(new Date())

    const [selectedRange, setSelectedRange] = useState<{
        start: number | null
        end: number | null
    }>({
        start: null,
        end: null
    })

    const year = currentDate.getFullYear()
    const month = currentDate.getMonth()

    const todayYear = today.getFullYear()
    const todayMonth = today.getMonth()
    const todayDate = today.getDate()

    const [isDragging, setIsDragging] = useState(false)

    // Get the minimum and maximum selected dates
    const minDate = selectedRange.start !== null && selectedRange.end !== null
        ? Math.min(selectedRange.start, selectedRange.end)
        : null

    const maxDate = selectedRange.start !== null && selectedRange.end !== null
        ? Math.max(selectedRange.start, selectedRange.end)
        : null

    const handleMonthChange = (direction: number) => {
        setCurrentDate(new Date(year, month + direction, 1))
    }

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

    const [isModalOpen, setIsModalOpen] = useState(false)

    const [hasDragged, setHasDragged] = useState(false)

    const [dragStart, setDragStart] = useState<number | null>(null)

    // Stop dragging when the mouse button is released
    useEffect(() => {
        const handleMouseUp = () => {
            setIsDragging(false)
        }

        window.addEventListener("mouseup", handleMouseUp)

        return () => {
            window.removeEventListener("mouseup", handleMouseUp)
        }
    }, [])

    // Clear selection when clicking outside the calendar
    useEffect(() => {
        const handleOutsideClick = (e: MouseEvent) => {
            if (
                calendarRef.current &&
                !calendarRef.current.contains(e.target as Node)
            ) {
                setSelectedRange({
                    start: null,
                    end: null
                })
            }
        }

        document.addEventListener("mousedown", handleOutsideClick)

        return () => {
            document.removeEventListener("mousedown", handleOutsideClick)
        }
    }, [])

    return (
        <div>
            <h1>DoTogether Calendar</h1>

            <div ref={calendarRef}>

                <div>
                    <button onClick={() => handleMonthChange(-1)}>Previous</button>
                    <h2>{year}년 {month + 1}월</h2>
                    <button onClick={() => handleMonthChange(1)}>Next</button>
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
                            onMouseDown={() => {
                                setIsDragging(true)
                                setHasDragged(false)
                                setDragStart(day)

                                setSelectedRange({
                                    start: day,
                                    end: day
                                })
                            }}

                            onClick={(e) => {
                                e.stopPropagation()

                                if (hasDragged) {
                                    return
                                }

                                if (
                                    minDate !== null &&
                                    maxDate !== null &&
                                    day >= minDate &&
                                    day <= maxDate
                                ) {
                                    setIsModalOpen(true)
                                } else {
                                    setSelectedRange({
                                        start: null,
                                        end: null
                                    })
                                }
                            }}

                            onMouseEnter={() => {
                                if (isDragging && dragStart !== null && dragStart !== day) {
                                    setHasDragged(true)

                                    setSelectedRange({
                                        start: dragStart,
                                        end: day
                                    })
                                }
                            }}

                            className={[
                                year === todayYear &&
                                    month === todayMonth &&
                                    day === todayDate
                                    ? 'today'
                                    : '',

                                minDate !== null &&
                                    maxDate !== null &&
                                    day >= minDate &&
                                    day <= maxDate
                                    ? 'selected'
                                    : ''
                            ].filter(Boolean).join(' ')}
                        >
                            {day}
                        </div>
                    ))}
                </div>

            </div>
            {isModalOpen && minDate !== null && maxDate !== null && (
                <ProjectModal
                    onClose={() => setIsModalOpen(false)}
                    year={year}
                    month={month}
                    startDate={minDate}
                    endDate={maxDate}
                />
            )}
        </div>
    )
}

export default Calendar
