window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        generate_pdf_function: function generatePDF(n_clicks) {
            var element = document.getElementById('simulation-container');
            var divHeight = element.clientHeight
            var divWidth = element.clientWidth
            var ratio = divHeight / divWidth;
            
            let pdf_orientation = 'p';
            if (divWidth>divHeight) {
                pdf_orientation = 'l';
            }
            var doc = new jsPDF(pdf_orientation,'px',[divWidth, divHeight]);
            var width = doc.internal.pageSize.width;
            var height = doc.internal.pageSize.height;
            
            var opt = {
                margin: 0,
                filename: 'simulation_report.pdf',
                image: { type: 'jpeg', quality: 1 },
                html2canvas: {
                    // scale: 2,
                    width: divWidth+50,
                    height: divHeight+50*ratio,
                    // windowWidth: divWidth,
                    // windowHeight: divHeight,
                    x: 0,
                    y: 0,
                    // scrollX: 0,
                    // scrollY: 0,
                },
                jsPDF: { 
                    unit: 'px', 
                    format: [divWidth, divHeight], 
                    orientation: pdf_orientation , 
                    hotfixes: ["px_scaling"]
                },
                // pagebreak: { mode: ['avoid-all', 
                //                     // 'css', 
                //                     // 'legacy'
                //                 ] }
            };

            html2pdf()
                .set(opt)
                .from(element)
                .toPdf()
                .get('pdf')
                // .then(function (pdf) {
                //     var totalPages = pdf.internal.getNumberOfPages();
                //     for (var i = 1; i <= totalPages; i++) {
                //         pdf.setPage(i);
                //         pdf.setFontSize(10);
                //         pdf.text('Page ' + i + ' of ' + totalPages, pdf.internal.pageSize.getWidth() - 50, pdf.internal.pageSize.getHeight() - 10);
                //     }
                // })
                .save();
        }
    }
});