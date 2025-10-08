# Cold Reads Stories - Weekly Update Guide

## How It Works

The newsletter now automatically displays the correct week's stories based on the current date! No need to edit `index.html` every week.

## What's Already Set Up

✅ **10 weeks pre-loaded** from October 6 through December 19, 2025
✅ **Skips break weeks**: Thanksgiving week and last two weeks of December
✅ **Automatic updates**: The page shows the right week's stories automatically

## Weekly Schedule

| Week Start | Stories Theme |
|------------|---------------|
| Oct 6-10   | Adventure stories (current) |
| Oct 13-17  | Mystery & exploration |
| Oct 20-24  | Halloween themed |
| Oct 27-31  | More Halloween fun |
| Nov 3-7    | Autumn & nature |
| Nov 10-14  | Gratitude & thanksgiving prep |
| Nov 17-21  | Thanksgiving history |
| ~~Nov 24-28~~ | **SKIP - Thanksgiving Break** |
| Dec 1-5    | Winter & snow |
| Dec 8-12   | Holiday traditions |
| Dec 15-19  | Holiday celebrations |
| ~~Dec 22-26~~ | **SKIP - Winter Break** |
| ~~Dec 29-Jan 2~~ | **SKIP - Winter Break** |

## How to Add More Weeks

1. **Open `stories.js`** in any text editor
2. **Copy this template** and add it to the bottom of the `storiesData` array:

```javascript
{
    weekStart: "2025-01-06",  // Monday's date (YYYY-MM-DD format)
    stories: [
        { day: "Monday", title: "Your Story Title", icon: "🎯", file: "cold-reads-weekX-monday.html" },
        { day: "Tuesday", title: "Your Story Title", icon: "🌟", file: "cold-reads-weekX-tuesday.html" },
        { day: "Wednesday", title: "Your Story Title", icon: "🚀", file: "cold-reads-weekX-wednesday.html" },
        { day: "Thursday", title: "Your Story Title", icon: "🎨", file: "cold-reads-weekX-thursday.html" },
        { day: "Friday", title: "Your Story Title", icon: "🎉", file: "cold-reads-weekX-friday.html" }
    ]
},
```

3. **Create the story HTML files** for each day (you can copy an existing one and modify it)
4. **Save** - the website will automatically use the new week when that date arrives!

## Tips

- Use the **Monday's date** for `weekStart`
- Choose fun **emojis** that match your story theme
- Make sure the **filename** in the `file` field matches your actual HTML file
- Don't forget the **comma** at the end of each week block (except the last one)

## Emoji Ideas for Stories

🐱 🐶 🦊 🐻 🐼 🦁 🐯 🦋 🐝 🐢 🦉 🦅 🦆 🐳 🐙 🦀
🌸 🌻 🌺 🌷 🌹 🌲 🌳 🌴 🍂 🍁 ☀️ 🌙 ⭐ ⚡ 🌈 ☁️
🎨 🎭 🎪 🎬 🎮 🎯 🎲 🎸 🎹 🎺 🎻 📚 ✏️ 📝 🔬 🔭
🏠 🏰 🏔️ 🗻 🏖️ 🏜️ 🗺️ 🧭 🚀 ✈️ 🚁 🚂 🚢 ⛵ 🎡 🎢
🍎 🍊 🍋 🍌 🍉 🍇 🍓 🍑 🥕 🌽 🥖 🥐 🧁 🍪 🍰 🎂
⚽ 🏀 🏈 ⚾ 🎾 🏐 🏓 🏸 🥏 🎿 ⛸️ 🛷 🏹 🎣 🏆 🥇

## Need Help?

If you have questions about updating the stories, just ask! The system is designed to be simple and flexible.

