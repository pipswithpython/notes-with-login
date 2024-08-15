window.onload = function() {
    if (document.body.scrollHeight > window.innerHeight) {
        window.scrollTo(0, document.body.scrollHeight);
    }
};

function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ noteId: noteId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(() => {
        window.location.reload();
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}
