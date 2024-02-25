document.addEventListener('DOMContentLoaded', () => {
    const grid = document.querySelector('#game-board');
    const startButton = document.getElementById('start-game');
    let cardsChosen = [];
    let cardsChosenId = [];
    let cardsWon = [];

    const cardArray = [
        // { name: 'card1', img: 'static/memegame/images/distracted.png' },
        // { name: 'card1', img: 'static/memegame/images/distracted.png' },
        // { name: 'card2', img: 'static/memegame/images/drake.png' },
        // { name: 'card2', img: 'static/memegame/images/drake.png' },
        // { name: 'card3', img: 'static/memegame/images/fine.png' },
        // { name: 'card3', img: 'static/memegame/images/fine.png' },
        // { name: 'card4', img: 'static/memegame/images/rollsafe.png' },
        // { name: 'card4', img: 'static/memegame/images/rollsafe.png' },
        { name: 'card5', img: 'static/memegame/images/success.png' },
        { name: 'card5', img: 'static/memegame/images/success.png' },

        { name: 'card6', img: 'static/memegame/images/dan1.png' },
        { name: 'card6', img: 'static/memegame/images/dan1.png' },
        { name: 'card7', img: 'static/memegame/images/dan2.png' },
        { name: 'card7', img: 'static/memegame/images/dan2.png' },
        { name: 'card8', img: 'static/memegame/images/dan3.png' },
        { name: 'card8', img: 'static/memegame/images/dan3.png' },
        { name: 'card9', img: 'static/memegame/images/dan4.png' },
        { name: 'card9', img: 'static/memegame/images/dan4.png' },
        { name: 'card10', img: 'static/memegame/images/dan5.png' },
        { name: 'card10', img: 'static/memegame/images/dan5.png' },
        { name: 'card11', img: 'static/memegame/images/dan6.png' },
        { name: 'card11', img: 'static/memegame/images/dan6.png' },
        { name: 'card12', img: 'static/memegame/images/dan7.png' },
        { name: 'card12', img: 'static/memegame/images/dan7.png' },
        
        // ...add more pairs as needed
    ];

    function shuffle(array) {
        array.sort(() => 0.5 - Math.random());
    }

    function createBoard() {
        shuffle(cardArray);
        grid.innerHTML = '';
        cardsWon = [];

        for (let i = 0; i < cardArray.length; i++) {
            const card = document.createElement('img');
            card.setAttribute('src', 'static/memegame/images/blank.png');
            card.setAttribute('data-id', i);
            card.style.width = '300px';  // Set the width as needed
            card.style.height = '300px'; // Set the height as needed
            card.addEventListener('click', flipCard);
            grid.appendChild(card);
        }
    }

    function flipCard() {
        let cardId = this.getAttribute('data-id');
        if (!cardsChosenId.includes(cardId)) {
            cardsChosen.push(cardArray[cardId].name);
            cardsChosenId.push(cardId);
            this.setAttribute('src', cardArray[cardId].img);
            if (cardsChosen.length === 2) {
                setTimeout(checkForMatch, 500);
            }
        }
    }

    function checkForMatch() {
        const cards = document.querySelectorAll('#game-board img');
        const firstCardId = cardsChosenId[0];
        const secondCardId = cardsChosenId[1];

        if (cardsChosen[0] === cardsChosen[1] && firstCardId !== secondCardId) {
            cards[firstCardId].style.visibility = 'hidden';
            cards[secondCardId].style.visibility = 'hidden';
            cards[firstCardId].removeEventListener('click', flipCard);
            cards[secondCardId].removeEventListener('click', flipCard);
            cardsWon.push(cardsChosen);
        } else {
            cards[firstCardId].setAttribute('src', 'static/memegame/images/blank.png');
            cards[secondCardId].setAttribute('src', 'static/memegame/images/blank.png');
        }

        cardsChosen = [];
        cardsChosenId = [];

        if (cardsWon.length === cardArray.length / 2) {
            alert('Congratulations! You found them all!');
        }
    }

    startButton.addEventListener('click', createBoard);
});
