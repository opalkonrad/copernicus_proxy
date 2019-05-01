jQuery(function ($) {
    const sliceType = {
        "years": -4,
        "months": -2,
        "days": -2,
    };

    function updateType(type) {
        let selectedList = [];
        let selectedOptions = $('.field--' + type).find('.dropped');
        for (let i = 0; i < selectedOptions.length; i++) {
            let tmpValue = selectedOptions.get(i).getAttribute('data-value');
            selectedList.push(("0" + tmpValue).slice(sliceType[type]));
        }
        $('.field--' + type).find('#id_' + type).val(JSON.stringify(selectedList));
    }

    function updateFormData() {
        updateType('years');
        updateType('months');
        updateType('days');
    }

    $('.selection__form')
        .drag("start", function (ev, dd) {
            return $('<div class="selection" />')
                .css('opacity', .65)
                .appendTo(document.body);
        })
        .drag(function (ev, dd) {
            $(dd.proxy).css({
                top: Math.min(ev.pageY, dd.startY),
                left: Math.min(ev.pageX, dd.startX),
                height: Math.abs(ev.pageY - dd.startY),
                width: Math.abs(ev.pageX - dd.startX)
            });
        })
        .drag("end", function (ev, dd) {
            $(dd.proxy).remove();
        });

    $('.drop')
        .drop("start", function () {
            $(this).addClass("active");
        })
        .drop(function (ev, dd) {
            $(this).toggleClass("dropped");
            $(this).closest('.field').find('.field__errors').html('');
            updateFormData();
        })
        .drop("end", function () {
            $(this)
                .removeClass("active")
                .removeClass("mouseupListener");
        })
        .on('mousedown', function (event) {
            if (event.which !== 1) return false;
            $(this).addClass("active");
            $(this).addClass("mouseupListener");
        })
        .on('mouseup', function () {
            $('.drop').removeClass('active');
            $('.mouseupListener')
                .toggleClass("dropped")
                .removeClass("mouseupListener");
            $(this).closest('.field').find('.field__errors').html('');
            updateFormData();
        });

    $.drop({multi: true});
    
    $('.field__button--select')
        .on('click', function () {
            $(this).closest('.field').find('.drop').addClass('dropped');
            $(this).closest('.field').find('.field__errors').html('');
            updateFormData();
        });
    $('.field__button--clear')
        .on('click', function () {
            $(this).closest('.field').find('.drop').removeClass('dropped');
            updateFormData();
        });
});