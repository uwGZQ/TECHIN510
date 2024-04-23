function addTodo() {
    const input = document.getElementById('todo-input');
    const todoText = input.value.trim();
    if (todoText !== '') {
        const li = document.createElement('li');
        li.textContent = todoText;
        li.onclick = function() { this.remove(); };
        document.getElementById('todo-list').appendChild(li);
        input.value = '';
    }
}
