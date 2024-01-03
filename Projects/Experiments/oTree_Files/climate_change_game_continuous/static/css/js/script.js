$(document).ready(function() {
    var bars = $('.progress-bar');
    var inputs = $('input[type=hidden]');
    var total = 100;

    // set initial progress values
    bars.each(function(index, bar) {
        $(bar).find('.progress').css('width', '9%');
        $(bar).find('.progress-label').text(index + 1);
        $(inputs[index]).val(9);
    });

    // update progress and input values on drag
    bars.on('mousedown', function(event) {
        var bar = $(this);
        var index = bars.index(bar);
        var startX = event.pageX;
        var startWidth = bar.find('.progress').width();

        $(document).on('mousemove', function(event) {
            var offset = event.pageX - startX;
            var width = Math.max(startWidth + offset, 0);
            var max = (index == bars.length - 1) ? total : parseInt(inputs[index + 1].value);
            var min = (index == 0) ? 0 : parseInt(inputs[index - 1].value);
            var diff = max - min;

            if (width > diff) {
                width = diff;
            }

            bar.find('.progress').css('width', width / total * 100 + '%');
            inputs[index].value = Math.round(width / total * 100);

            event.preventDefault();
        });

        $(document).on('mouseup', function() {
            $(document).off('mousemove');
            $(document).off('mouseup');
        });

        event.preventDefault();
    });
});

