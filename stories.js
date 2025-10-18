// Cold Reads Stories Configuration
// Add new weeks here - the system will automatically display the correct week based on the current date

const storiesData = [
    // OCTOBER 2025
    {
        weekStart: "2025-10-06",  // Week of Oct 6-10
        stories: [
            { day: "Monday", title: "The Wise Spider", icon: "🐱", file: "cold-reads-practice.html" },
            { day: "Tuesday", title: "The Magic Garden", icon: "🌸", file: "cold-reads-tuesday.html" },
            { day: "Wednesday", title: "The Science Fair", icon: "🔬", file: "cold-reads-wednesday.html" },
            { day: "Thursday", title: "The Brave Firefighter", icon: "🚒", file: "cold-reads-thursday.html" },
            { day: "Friday", title: "The Weekend Adventure", icon: "🏔️", file: "cold-reads-friday.html" }
        ]
    },
    {
        weekStart: "2025-10-13",  // Week of Oct 13-17
        stories: [
            { day: "Monday", title: "The Mysterious Cave", icon: "🕳️", file: "cold-reads-week2-monday.html" },
            { day: "Tuesday", title: "The Flying Machine", icon: "✈️", file: "cold-reads-week2-tuesday.html" },
            { day: "Wednesday", title: "The Lost Puppy", icon: "🐕", file: "cold-reads-week2-wednesday.html" },
            { day: "Thursday", title: "The Rainbow Bridge", icon: "🌈", file: "cold-reads-week2-thursday.html" },
            { day: "Friday", title: "The Treasure Hunt", icon: "🗺️", file: "cold-reads-week2-friday.html" }
        ]
    },
    {
        weekStart: "2025-10-18",  // Week of Oct 20-24
        stories: [
            { day: "Monday", title: "How Butterflies Grow", icon: "🦋", file: "cold-reads-week3-monday.html" },
            { day: "Tuesday", title: "The Legend of the Rainbow", icon: "🌈", file: "cold-reads-week3-tuesday.html" },
            { day: "Wednesday", title: "Amazing Animal Adaptations", icon: "🐫", file: "cold-reads-week3-wednesday.html" },
            { day: "Thursday", title: "King Midas and the Golden Touch", icon: "👑", file: "cold-reads-week3-thursday.html" },
            { day: "Friday", title: "The Life of a Bee", icon: "🐝", file: "cold-reads-week3-friday.html" }
        ]
    }
];

// Function to get the current week's stories
function getCurrentWeekStories() {
    const today = new Date();
    today.setHours(0, 0, 0, 0); // Reset time to midnight for accurate comparison
    
    console.log('Today:', today.toDateString(), 'Looking for matching week...');
    
    // Find the week that matches the current date
    for (let i = 0; i < storiesData.length; i++) {
        const weekStart = new Date(storiesData[i].weekStart);
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekEnd.getDate() + 6); // Add 6 days to get the end of the week
        
        console.log(`Week ${i+1}: ${weekStart.toDateString()} to ${weekEnd.toDateString()}`);
        
        if (today >= weekStart && today <= weekEnd) {
            console.log('✓ Found matching week!', storiesData[i].stories[0].title);
            return storiesData[i];
        }
    }
    
    // If no matching week found, return the last (most recent) week as default
    console.log('No match found, using most recent week');
    return storiesData[storiesData.length - 1];
}

// Function to update the daily reading buttons
function updateDailyReadingButtons() {
    const currentWeek = getCurrentWeekStories();
    const buttons = document.querySelectorAll('.daily-btn');
    
    if (buttons.length === 5 && currentWeek.stories.length === 5) {
        buttons.forEach((button, index) => {
            const story = currentWeek.stories[index];
            
            // Update the link
            button.href = story.file;
            
            // Update the icon
            const iconElement = button.querySelector('.day-icon');
            if (iconElement) {
                iconElement.textContent = story.icon;
            }
            
            // Update the story title
            const titleElement = button.querySelector('.story-title');
            if (titleElement) {
                titleElement.textContent = story.title;
            }
        });
    }
}

// Run the update when the page loads
document.addEventListener('DOMContentLoaded', updateDailyReadingButtons);

