// getCookie function from Django Docs
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Generate human-readable list of authors from the array of authors provided by the API
const authorsFormatter = new Intl.ListFormat('en', { style: 'long', type: 'conjunction' });

function handleAddBook() {
    const addBookButtons = document.querySelectorAll('#add-book-button');

    addBookButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const bookDataString = event.target.getAttribute('data-book');
            const bookDataArray = bookDataString.split('&+');
            const bookDataObject = {
                cover: bookDataArray[0],
                title: bookDataArray[1],
                authors: bookDataArray[2],
                isbn13: bookDataArray[3]
            };

            let formData = new FormData();

            for (let k in bookDataObject) {
                formData.append(k, bookDataObject[k]);
            }

            const endpoint = '/books/add/'

            const csrftoken = getCookie('csrftoken');

            const options = {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            }

            fetch(endpoint, options)
                .then((r) => r.json())
                .then((result) => {
                    if (result.status === 200) {
                        window.location = '/books/'
                    } else {
                        alert('Something has gone wrong. Please try again.')
                    }
                });
        })
    })
}

(async function handleBookSearch() {
    const form = document.querySelector('form#book-search');
    const input = document.querySelector('[name=search_term]');
    const resultsDiv = document.querySelector('#books');
    const searchButton = document.querySelector('#search-books');

    form.addEventListener('submit', (event) => {
        searchButton.innerHTML = 'Searching...'

        event.preventDefault();

        const searchValue = input.value;

        const options = {
            headers: {
                // I know...
                'Authorization': '43822_7d36594b478c81f4aaed821554795aef'
            }
        }

        // const proxy = '/books/add/isbndb-proxy/?url=https://api2.isbndb.com/books/${searchValue}?pageSize=5'

        // fetch(proxy, options)
        //     .then((r) => r.json())
        //     .then((result) => {
        //         console.log(result);
        //     });

        fetch(`https://api2.isbndb.com/books/${searchValue}?pageSize=5`, options)
            .then((r) => r.json())
            .then((result) => {               
                let html = '';
                result.books.forEach(book => {
                    const authors = authorsFormatter.format(book.authors);
                    
                    html += `
                        <div class="book">
                            <div class="cover">
                                <img class="cover" src="${book.image}" alt="${book.title} cover">
                            </div>
                            <div class="info">
                                <p class="title"><strong><a target="_blank" href="https://isbndb.com/book/${book.isbn13}">${book.title}</a></strong></p>
                                <p class="authors">Written by ${authors}</p>
                                <p class="isbn">ISBN13: ${book.isbn13}</p>
                                <button style="margin-top: 20px;" type="button" data-book="${book.image}&+${book.title}&+${authors}&+${book.isbn13}" id="add-book-button">Add to Book List</button>
                            </div>
                        </div>
                    `
                })
                resultsDiv.innerHTML = html;
                handleAddBook();
                searchButton.innerHTML = 'Search Books'
            })
            .catch(error => {
                searchButton.innerHTML = 'Search Books'
                console.error(error);
            });
    })
})();