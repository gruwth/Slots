fetch('/balance/' + localStorage.getItem('user_id'))
    .then(response => response.json())
    .then(data => {
        document.getElementById('balance').innerText = `Balance: ${data.balance}`;
    });
        
function play(stake) {
    fetch('/play', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: localStorage.getItem('user_id'), stake: parseInt(stake) })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('balance').innerText = `Balance: ${data.balance}`;
            const symbolsContainer = document.getElementById('symbols');
            symbolsContainer.innerHTML = 'Symbols: ';

            const symbolCounts = {};
            data.slots.forEach(symbol => {
                if (symbolCounts[symbol]) {
                    symbolCounts[symbol]++;
                } else {
                    symbolCounts[symbol] = 1;
                }
            });

            const mostOccurringSymbol = Object.keys(symbolCounts).reduce((a, b) => symbolCounts[a] > symbolCounts[b] ? a : b);

            data.slots.forEach(symbol => {
                const symbolElement = document.createElement('p');
                symbolElement.innerText = symbol;
                if (symbol === mostOccurringSymbol) {
                    symbolElement.id = 'winning-symbol';
                }
                symbolsContainer.appendChild(symbolElement);
            });
            document.getElementById('win_amount').innerText = `You won: ${data.win_amount}`;
        } else {
            alert('Insufficient balance');
        }
    });
}


