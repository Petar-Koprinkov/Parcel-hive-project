document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    socket.on('connect', () => {
        document.getElementById('status').innerText = 'Status: Connected';
    });

    socket.on('mouse_click', (data) => {
        const eventList = document.getElementById('events');
        const newEvent = document.createElement('li');
        newEvent.innerText = `Mouse clicked at (${data.x}, ${data.y})`;
        eventList.appendChild(newEvent);
    });
});
