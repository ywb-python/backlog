window.Superlists = {};
window.Superlists.initialize = function () {
    console.log('initialize called');
    $('input[name="text"]').on('keypress', function () {
        $('.has-error').hide();
    });
};

