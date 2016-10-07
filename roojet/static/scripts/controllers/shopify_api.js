'use strict'

/**
 * @ngdoc function
 * @name frontApp.controller:CommentsController
 * @description
 * # CommentsController
 * Controller of the application
 * Handles information from the API to be connected with the view
 */

angular.module('ROO').controller('ShopifyController', ['$scope', function ($scope) {
    $scope.historic_chart = function(product_id, historic, title) {
        var e = document.getElementById("variable")
        var select = e.options[e.selectedIndex].value
        var label_set = []
        var data_set = []
        for (var index = 0; index < historic.length; ++index) {
            var obj = historic[index]
            if (obj['fields']['Product'] == product_id){
                label_set.push(obj['fields']['date'])
                if(select == 'profit'){
                    data_set.push(obj['fields']['total'])                   
                }
                if(select == 'revenue'){
                    data_set.push(obj['fields']['quantity'])                   
                }
            }
        }

        var data = {
            labels: label_set,
            datasets: [
            {
                label: "Product Optimization",
                fillColor: "rgba(129,215,66,.5)",
                strokeColor: "rgba(129,215,66,.8)",
                pointColor: "rgba(129,215,66,.8)",
                pointStrokeColor: "#81D742",
                pointHighlightFill: "#81D742",
                pointHighlightStroke: "rgba(129,215,66,.5)",
                data: data_set
            }
            ]
        }

        if ($(`#myModal${product_id}`).length) {
            $(`#myModal${product_id}`).on('shown.bs.modal', function (event) {
                var ctx = document.getElementById(`mychart${product_id}`)
                new Chart(ctx.getContext('2d')).Line(data)
            })
        } else {
            var content = document.createElement('div'),
            widget = document.createElement('div'),
            body = document.body.childNodes[3],
            canvasElement = document.createElement('canvas'),
            modal = document.createElement('div')

            modal.structure = {
                dialog: document.createElement('div'),
                content: document.createElement('div'),
                header: document.createElement('div'),
                title: document.createElement('h4'),
                close: document.createElement('button'),
                body: document.createElement('div')
            }

            modal.className = 'modal fade in'
            modal.id = `myModal${product_id}`
            modal.setAttribute('role', 'dialog')
            modal.structure.close.setAttribute('data-dismiss', 'modal')
            modal.structure.close.innerHTML = 'x'
            modal.structure.title.innerHTML = String(title)
            canvasElement.id = `mychart${product_id}`
            canvasElement.className = 'mychart'
            modal.structure.dialog.className = 'modal-dialog'
            modal.structure.content.className = 'modal-content'
            modal.structure.header.className = 'modal-header'
            modal.structure.title.className = 'modal-title'
            modal.structure.body.className = 'modal-body'
            modal.structure.close.className = 'close'
            content.className = 'chart'
            widget.className = 'chart-widget'

            body.appendChild(modal)
            modal.appendChild(modal.structure.dialog)
            modal.structure.dialog.appendChild(modal.structure.content)
            modal.structure.content.appendChild(modal.structure.header)
            modal.structure.content.appendChild(modal.structure.body)
            modal.structure.header.appendChild(modal.structure.close)
            modal.structure.header.appendChild(modal.structure.title)
            modal.structure.body.appendChild(content)
            content.appendChild(widget)
            widget.appendChild(canvasElement)
            $(`#myModal${product_id}`).on('shown.bs.modal', function (event) {
                var Linectx = new Chart(canvasElement.getContext('2d')).Line(data)
            })
        }
    }

    function generateLabelsFromData(historic) {
        var labels = []
        for (var index = 0; index < historic.length; ++index) {
            var obj = historic[index]
            if (labels.indexOf(obj['fields']['date']) == -1){
                labels.push(obj['fields']['date'])
            }
        }
        return labels
    }
    function generateDataSetsFromData(products_serialized, historic) {
        var datasets = []
        var labels = generateLabelsFromData(historic)
        for (var index_p = 0; index_p < products_serialized.length; ++index_p) {
            var new_data = []
            var product = products_serialized[index_p]
            for (var index_d = 0; index_d < labels.length; ++index_d){
                var cont = 0
                for (var index_h = 0; index_h < historic.length; ++index_h){
                    var hist = historic[index_h]
                    if (hist['fields']['Product'] == product['pk'] && hist['fields']['date'] == labels[index_d]){
                        cont = hist['fields']['quantity']
                    }
                }
                new_data[index_d] = cont
            }
            datasets[datasets.length] = new_data
        }
        return datasets
    }

    $scope.total_chart = function(products_serialized, historic) {
        // $scope.labels = generateLabelsFromData(historic)
        // TODO hide labels in a different way
        $scope.labels = [];
        for (i in generateLabelsFromData(historic)){
            $scope.labels.push("");
        };
        var dataset = generateDataSetsFromData(products_serialized, historic)
        var series=[["Total sells"]]
        var total_data=[]
        for (var i = 0; i < dataset[0].length; i++) total_data[i] = 0;
        for (var index_d = 0; index_d < dataset.length; ++index_d){
            var product_data = dataset[index_d]
            for (var index_p = 0; index_p < product_data.length; ++index_p){
                total_data[index_p] = total_data[index_p] + product_data[index_p]
            }
        }
        $scope.data = [total_data];
        $scope.series=series;
        $scope.colours = [{fillColor: 'rgba(255,255,255,.5)', strokeColor: 'rgba(129,215,66,.8)'}];
    }
}])


