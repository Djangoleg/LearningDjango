window.addEventListener("load", () => {

    $( document ).on( 'click', '.details a', (e) => {
       if (e.target.hasAttribute('href')) {
           let link = e.target.href + 'ajax/';
           let link_array = link.split('/');
           if (link_array[4] == 'category') {
               $.ajax({
                   url: link,
                   success: function (data) {
                       $('.details').html(data.result);
                   },
               });

               e.preventDefault();
           }
       }
    });

},false);


