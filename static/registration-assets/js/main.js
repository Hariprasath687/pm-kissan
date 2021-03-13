(function($) {



    var form = $("#signup-form");
    form.validate({
        errorPlacement: function errorPlacement(error, element) {
            element.before(error);
        },
        rules: {
            email: {
                email: true
            }
        },
        onfocusout: function(element) {
            $(element).valid();
        },
    });
    form.children("div").steps({
        headerTag: "h3",
        bodyTag: "fieldset",
        transitionEffect: "fade",
        stepsOrientation: "vertical",
        titleTemplate: '<div class="title"><span class="step-number">#index#</span><span class="step-text">#title#</span></div>',
        labels: {
            previous: 'Previous',
            next: 'Next',
            finish: 'Finish',
            current: ''
        },
        onStepChanging: function(event, currentIndex, newIndex) {
            if (currentIndex === 0) {
                form.parent().parent().parent().append('<div class="footer footer-' + currentIndex + '"></div>');
            }
            if (currentIndex === 1) {
                form.parent().parent().parent().find('.footer').removeClass('footer-0').addClass('footer-' + currentIndex + '');
            }
            if (currentIndex === 2) {
                form.parent().parent().parent().find('.footer').removeClass('footer-1').addClass('footer-' + currentIndex + '');
            }
            if (currentIndex === 3) {
                form.parent().parent().parent().find('.footer').removeClass('footer-2').addClass('footer-' + currentIndex + '');
            }
            // if(currentIndex === 4) {
            //     form.parent().parent().parent().append('<div class="footer" style="height:752px;"></div>');
            // }
            form.validate().settings.ignore = ":disabled,:hidden";
            return form.valid();
        },
        onFinishing: function(event, currentIndex) {
            form.validate().settings.ignore = ":disabled";
            return form.valid();
        },
        onFinished: function(event, currentIndex) {
            alert('Submited');
        },
        onStepChanged: function(event, currentIndex, priorIndex) {

            return true;
        }
    });

    jQuery.extend(jQuery.validator.messages, {
        required: "",
        remote: "",
        email: "",
        url: "",
        date: "",
        dateISO: "",
        number: "",
        digits: "",
        creditcard: "",
        equalTo: ""
    });

    $.dobPicker({
        daySelector: '#birth_date',
        monthSelector: '#birth_month',
        yearSelector: '#birth_year',
        dayDefault: '',
        monthDefault: '',
        yearDefault: '',
        minimumAge: 0,
        maximumAge: 120
    });
    var marginSlider = document.getElementById('slider-margin');
    if (marginSlider != undefined) {
        noUiSlider.create(marginSlider, {
              start: [1100],
              step: 100,
              connect: [true, false],
              tooltips: [true],
              range: {
                  'min': 100,
                  'max': 2000
              },
              pips: {
                    mode: 'values',
                    values: [100, 2000],
                    density: 4
                    },
                format: wNumb({
                    decimals: 0,
                    thousand: '',
                    prefix: '$ ',
                })
        });
        var marginMin = document.getElementById('value-lower'),
	    marginMax = document.getElementById('value-upper');

        marginSlider.noUiSlider.on('update', function ( values, handle ) {
            if ( handle ) {
                marginMax.innerHTML = values[handle];
            } else {
                marginMin.innerHTML = values[handle];
            }
        });
    }
})(jQuery);
function addRow() {
    "use strict";
 
     var table = document.getElementById("table");
     var td1 = document.createElement("td");
     var td2 = document.createElement("td");
     var td3 = document.createElement("td");    
 
     td1.innerHTML = document.getElementById("item").value;
     td2.innerHTML  = document.getElementById("quantity").value;
     td3.innerHTML  = document.getElementById("price").value;
 
     row.appendChild(td1);
     row.appendChild(td2);
     row.appendChild(td3);
 
     table.children[0].appendChild(row);
 };

// var myselect = document.getElementById('myselect');

// function createOption() {
//     var currentText = document.getElementById('mytext').value;
//     var objOption = document.createElement("option");
//     objOption.text = currentText;
//     objOption.value = currentText;

//     //myselect.add(objOption);
//     myselect.options.add(objOption);
// }

// function editOption() {
//     myselect.options[myselect.selectedIndex].text = document.getElementById('mytext').value;
//     myselect.options[myselect.selectedIndex].value = document.getElementById('mytext').value;
// }

// function deleteOption() {
//     myselect.options[myselect.selectedIndex] = null;
//     if (myselect.options.length == 0) document.getElementById('mytext').value = '';
//     else document.getElementById('mytext').value = myselect.options[myselect.selectedIndex].text;
// }

// document.getElementById('addbtn').onclick = createOption;
// document.getElementById('editbtn').onclick = editOption;
// document.getElementById('deletebtn').onclick = deleteOption;

// myselect.onchange = function() {
//     document.getElementById('mytext').value = myselect.value;
// }

// var stateObject = {
//     "India": { "Delhi": ["new Delhi", "North Delhi"],
//     "Kerala": ["Thiruvananthapuram", "Palakkad"],
//     "Goa": ["North Goa", "South Goa"],
//     },
//     "Australia": {
//     "South Australia": ["Dunstan", "Mitchell"],
//     "Victoria": ["Altona", "Euroa"]
//     }, "Canada": {
//     "Alberta": ["Acadia", "Bighorn"],
//     "Columbia": ["Washington", ""]
//     },
//     }
//     window.onload = function () {
//     var countySel = document.getElementById("countySel"),
//     stateSel = document.getElementById("stateSel"),
//     districtSel = document.getElementById("districtSel");
//     for (var country in stateObject) {
//     countySel.options[countySel.options.length] = new Option(country, country);
//     }
//     countySel.onchange = function () {
//     stateSel.length = 1; // remove all options bar first
//     districtSel.length = 1; // remove all options bar first
//     if (this.selectedIndex < 1) return; // done
//     for (var state in stateObject[this.value]) {
//     stateSel.options[stateSel.options.length] = new Option(state, state);
//     }
//     }
//     countySel.onchange(); // reset in case page is reloaded
//     stateSel.onchange = function () {
//     districtSel.length = 1; // remove all options bar first
//     if (this.selectedIndex < 1) return; // done
//     var district = stateObject[countySel.value][this.value];
//     for (var i = 0; i < district.length; i++) {
//     districtSel.options[districtSel.options.length] = new Option(district[i], district[i]);
//     }
//     }
//     }