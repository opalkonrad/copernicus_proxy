jQuery(function ($) {
    const numericTypes = ["years", "months", "days"];
    const sliceType = {
        "years": -4,
        "months": -2,
        "days": -2,
    };

    function updateType(type) {
        let selectedList = [];
        if (type in numericTypes) {
            let selectedOptions = $('.field--' + type).find('.dropped');
            for (let i = 0; i < selectedOptions.length; i++) {
                let tmpValue = selectedOptions.get(i).getAttribute('data-value');
                selectedList.push(("0" + tmpValue).slice(sliceType[type]));
            }
            $('#id_' + type).val(JSON.stringify(selectedList));
        } else if (type === "filters") {
            let category = $('.filter__select').val();
            let selectedOptions = $('.filters--' + category).find('.dropped:not(.active)');
            selectedOptions.each(function () {
                let currentValue = $(this).attr('data-value');
                let selectedOptions = $('.filters--' + category).find('.dropped:not(.active)');
                $('filters__container').find('');
                $(this).parent().detach().appendTo('.filters__selected .filters--' + category + ' .selection__container--list');

                let unselectedOptions = $('.filters--' + category).find('.drop:not(.dropped):not(.active)');
            });
            let unselectedOptions = $('.filters--' + category).find('.drop:not(.dropped):not(.active)');
            unselectedOptions.each(function () {
                $(this).parent().detach().appendTo('.filters__options .filters--' + category + ' .selection__container--list');
            });
        }
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

    $('.drop:not(.selection__filters)')
        .drop("start", function () {
            $(this).addClass("active");
        })
        .drop(function (ev, dd) {
            $(this).toggleClass("dropped");
            $(this).closest('.field').find('.field__errors').html('');
        })
        .drop("end", function () {
            $(this)
                .removeClass("active")
                .removeClass("mouseupListener");
            updateFormData();
        })
        .on('mousedown', function (event) {
            if (event.which !== 1) return false;
            $(this).addClass("active");
            $(this).addClass("mouseupListener");
        })
        .on('mouseup', function () {
            $(this).removeClass('active');
            $('.mouseupListener')
                .toggleClass("dropped")
                .removeClass("mouseupListener");
            $(this).closest('.field').find('.field__errors').html('');
            updateFormData();
        });

    $('.drop.selection__filters')
        .drop("start", function () {
            $(this).addClass("active");
        })
        .drop(function (ev, dd) {
            $(this).toggleClass("dropped");
            $(this).closest('.field').find('.field__errors').html('');
        })
        .drop("end", function () {
            $(this)
                .removeClass("active")
                .removeClass("mouseupListener");
            updateType('filters');
        })
        .on('mousedown', function (event) {
            if (event.which !== 1) return false;
            $(this).addClass("active");
            $(this).addClass("mouseupListener");
        })
        .on('mouseup', function () {
            $(this).removeClass('active');
            $('.mouseupListener')
                .toggleClass("dropped")
                .removeClass("mouseupListener");
            $(this).closest('.field').find('.field__errors').html('');
            updateType('filters');
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
    $('.field--filters')
        .on('click', '.field__button--show', function () {
            let filtersType = $(this).attr('data-filters');
            $(this).addClass('field__button--hide');
            $(this).removeClass('field__button--show');
            $(this).html('Hide');
            $(this).closest('.field--filters').find('.filters__' + filtersType).show();
        })
        .on('click', '.field__button--hide', function () {
            let filtersType = $(this).attr('data-filters');
            $(this).addClass('field__button--show');
            $(this).removeClass('field__button--hide');
            $(this).html('Show');
            $(this).closest('.field--filters').find('.filters__' + filtersType).hide();
        });

    $('.filter__select').on('change', function () {
        let category = $(this).val();
        $('.filters__container .selection__form').hide();
        if (category !== "--") {
            $('.filters__container').show();
            $('.filters__container .selection__form[data-category="' + category + '"]').show();
        } else {
            $('.filters__container').hide();
        }
    });
})
;