var limit = 20; // Max question
var count = 1; // There are 4 questions already

function addQuestion()
{
    var table = document.getElementById('select-range-table');
    if (table)
    {
        if (count < limit)
        {
            var di = document.createElement('div');
            var di2 = document.createElement('div');
            var di3 = document.createElement('div');
            di2.setAttribute("class", "customSelect");
            di3.style.padding = "2rem";
            var linebreak = document.createElement("br");
            var select = document.createElement('select');
            select.id = "select" + count;
            select.name = "select" + count;
            select.class = "select";
            select.options[0] = new Option("--Please choose an issue--", "");
            select.options[0].disabled = true;
            select.options[1] = new Option("Abortion is a woman's unrestricted right", "0");
            select.options[2] = new Option("Legally require hiring women & minorities", "1");
            select.options[3] = new Option("Comfortable with same-sex marriage", "2");
            select.options[4] = new Option("Keep God in the public sphere", "3");
            select.options[5] = new Option("Expand ObamaCare", "4");
            select.options[6] = new Option("Privatize Social Security", "5");
            select.options[7] = new Option("Vouchers for school choice", "6");
            select.options[8] = new Option("Fight EPA regulatory over-reach", "7");
            select.options[9] = new Option("Stricter punishment reduces crime", "8");
            select.options[10] = new Option("Absolute right to gun ownership", "9");
            select.options[11] = new Option("Higher taxes on the wealthy", "10");
            select.options[12] = new Option("Pathway to citizenship for illegal aliens", "11");
            select.options[13] = new Option("Support & expand free trade", "12");
            select.options[14] = new Option("Support American Exceptionalism", "13");
            select.options[15] = new Option("Expand the military", "14");
            select.options[16] = new Option("Make voter registration easier", "15");
            select.options[17] = new Option("Avoid foreign entanglements", "16");
            select.options[18] = new Option("Prioritize green energy", "17");
            select.options[19] = new Option("Marijuana is a gateway drug", "18");
            select.options[20] = new Option("Stimulus better than market-led recovery", "19");
            select.value = "";

            var range = document.createElement('input');
            range.class = "range";
            range.name = "range" + count;
            range.id = 'range' + count;
            range.type = 'range';
            range.value = '3';
            range.min = '1';
            range.max = '5';
            range.step = '1';

            var label = document.createElement('p');
            label.id = 'label' + count;
            label.innerHTML = "Neutral"
            label.style.paddingLeft = "5px";
            range.onchange = function() {updateVal(range.id,label.id)};
            label.style.color = "#ffffff";

            function updateVal(range,label){
              var slider = document.getElementById(range);
              var output = document.getElementById(label);
              if(slider.value==3){
                output.innerHTML = "Neutral";

              }
              else if(slider.value==1){
                output.innerHTML = "Strongly Oppose";
              }
              else if(slider.value==2){
                output.innerHTML = "Oppose";
              }
              else if(slider.value==5){
                output.innerHTML = "Strongly Favor";
              }
              else if(slider.value==4){
                output.innerHTML = "Favor";
              }
            };

            // Good practice to do error checking
            if (select && range)
            {
                var row = table.insertRow(-1)
                var cell1 = row.insertCell(0)
                var cell2 = row.insertCell(1)
                di2.appendChild(select);
                di3.append(di2);
                cell1.appendChild(di3);
                di.appendChild(range);
                cell2.appendChild(di);
                cell2.appendChild(label);
                // Increment the count
                count++;
            }

        }
        else
        {
            alert('Maximum Number of fields reached!');
        }
    }
}
