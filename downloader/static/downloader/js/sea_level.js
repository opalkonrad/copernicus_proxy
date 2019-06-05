jQuery(function ($) {
    const numericTypes = ["years", "months", "days"];
    const sliceType = {
        "years": -4,
        "months": -2,
        "days": -2,
    };

    function getType(type) {
        let value = $('#id_' + type).val();
        if (value)
            return JSON.parse(value);
        else
            return "";
    }

    function getFormat(type) {
        let value = $('input[name="' + type + '"]:checked').val();
        if (value)
            return value;
        else
            return "";
    }

    function updateType(type) {
        let selectedList = [];
        if (type === "filters") {
            let category = $('.filter__select').val();
            let selectedOptions = $('.filters__options .filters--' + category).find('.dropped:not(.active)');
            selectedOptions.each(function () {
                let currentValue = $(this).attr('data-value');
                let sameSelectedOptions = $('.filters__container .filters__options').find('li[data-value="' + currentValue + '"]');
                sameSelectedOptions.each(function () {
                    let localCategory = $(this).attr('data-category');
                    $(this).addClass('dropped');
                    $(this).parent().detach().appendTo('.filters__selected .filters--' + localCategory + ' .selection__container--list');
                });
            });
            let unselectedOptions = $('.filters__selected .filters--' + category).find('.drop:not(.dropped):not(.active)');
            unselectedOptions.each(function () {
                let currentValue = $(this).attr('data-value');
                let sameUnselectedOptions = $('.filters__container .filters__selected').find('li[data-value="' + currentValue + '"]');
                sameUnselectedOptions.each(function () {
                    let localCategory = $(this).attr('data-category');
                    $(this).removeClass('dropped');
                    $(this).parent().detach().appendTo('.filters__options .filters--' + localCategory + ' .selection__container--list');
                });
            });
        } else {
            let selectedOptions = $('.field--' + type).find('.dropped');
            for (let i = 0; i < selectedOptions.length; i++) {
                let tmpValue = selectedOptions.get(i).getAttribute('data-value');
                if (numericTypes.includes(type))
                    selectedList.push(("0" + tmpValue).slice(sliceType[type]));
                else
                    selectedList.push(tmpValue);
            }
            $('#id_' + type).val(JSON.stringify(selectedList));
        }
    }

    function updateFormData() {
        updateType('years');
        updateType('months');
        updateType('days');
        updateType('hours');
        updateType('filters');
        updateType('product_types');
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

    $('#dataset_select').on('change', function () {
        let dataset = $(this).val();
        if (dataset === 'reanalysis-era5-single-levels') {
            $('.field').show();
            $('.field--format_sea_level').hide();
        } else if (dataset === 'satellite-sea-level-mediterranean') {
            $('.field').show();
            $('.field--filters').hide();
            $('.field--product_types').hide();
            $('.field--hours').hide();
            $('.field--format_era5').hide();
        }
    });

    $('#submit').click(function (event) {
        event.preventDefault();
        let dataset = $('#dataset_select').val();
        let dictionary;
        let formData = [];
        formData.push(dataset);
        switch (dataset) {
            case 'reanalysis-era5-single-levels':
                dictionary = {
                    product_type: getType('product_types'),
                    variable: getType('filters'),
                    year: getType('years'),
                    month: getType('months'),
                    day: getType('days'),
                    time: getType('hours'),
                    format: getFormat('format_era5')
                };
                formData.push(dictionary);
                break;
            case 'satellite-sea-level-mediterranean':
                dictionary = {
                    variable: "all",
                    year: getType('years'),
                    month: getType('months'),
                    day: getType('days'),
                    format: getFormat('format_sea_level')
                };
                formData.push(dictionary);
                break;
        }
        console.log(JSON.stringify(formData));
    });
});