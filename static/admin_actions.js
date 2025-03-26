// admin_actions.js

(function($) {
    $(document).ready(function() {
        // Ajouter une boîte de dialogue de confirmation pour l'action Approuver
        $('a#action-approve').on('click', function(e) {
            e.preventDefault();
            if (confirm("Êtes-vous sûr de vouloir approuver cette permission ?")) {
                var href = $(this).attr('href');
                window.location.href = href;
            }
        });

        // Ajouter une boîte de dialogue de confirmation pour l'action Rejeter
        $('a#action-reject').on('click', function(e) {
            e.preventDefault();
            if (confirm("Êtes-vous sûr de vouloir rejeter cette permission ?")) {
                var href = $(this).attr('href');
                window.location.href = href;
            }
        });
    });
})(django.jQuery);
