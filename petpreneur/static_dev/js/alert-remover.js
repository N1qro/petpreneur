document.addEventListener("click", function(e) {
    var target = e.target.closest("#navbar--message--close--button");
 
    if (target) {
        var messageContainer = document.getElementById("navbar--message");
        if (messageContainer != null) {
            messageContainer.style.display = 'none';
        }
    }
 });
 