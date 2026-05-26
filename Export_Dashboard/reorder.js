const fs = require('fs');
const file = 'd:\\Zap Projects\\I love BanhMi\\Export_Dashboard\\Bao_Gia_Tong_Hop.html';
let content = fs.readFileSync(file, 'utf8');

const startMarker = '<div class="grid-container">';
const endMarker = '    </div>\n\n    <div class="note-bar"';

const startIndex = content.indexOf(startMarker) + startMarker.length;
const endIndex = content.indexOf(endMarker);

let gridContent = content.substring(startIndex, endIndex);

let parts = gridContent.split('<!-- THẺ ');
parts.shift(); // remove empty first part

let cards = parts.map(p => {
    let match = p.match(/^(\d+):/);
    let num = match ? parseInt(match[1]) : 0;
    return { num, content: '<!-- THẺ ' + p };
});

// Desired order of original IDs:
let order = [1, 2, 3, 13, 4, 5, 6, 7, 8, 9, 10, 11, 12];
let orderedCards = [];
for(let id of order) {
    let card = cards.find(c => c.num === id);
    if(card) orderedCards.push(card);
}

for (let i = 0; i < orderedCards.length; i++) {
    let newNum = i + 1;
    let oldNum = orderedCards[i].num;
    
    // update <!-- THẺ N:
    orderedCards[i].content = orderedCards[i].content.replace(new RegExp('<!-- THẺ ' + oldNum + ':'), '<!-- THẺ ' + newNum + ':');
    
    // update the title
    orderedCards[i].content = orderedCards[i].content.replace(new RegExp('<div class="category-title">\\s*' + oldNum + '\\.\\s*'), '<div class="category-title">\n            ' + newNum + '. ');
}

let newGridContent = '\n      ' + orderedCards.map(c => c.content).join('');
let newContent = content.substring(0, startIndex) + newGridContent + content.substring(endIndex);

fs.writeFileSync(file, newContent, 'utf8');
console.log('Reordered successfully');
