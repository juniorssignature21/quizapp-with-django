function markOnlyThis(clickedButton) {
    // Remove 'marked' class from all buttons
    const allButtons = document.querySelectorAll('.markable{{q.id}}');
    allButtons.forEach(input => input.classList.remove('marked'));
  
    // Add 'marked' class to the clicked one
    clickedButton.classList.add('marked');
  }