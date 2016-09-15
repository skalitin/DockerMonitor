function processResponse(data) {
    var containers = data.containers;
    var networks = data.networks;
    
    var nodes = [];
    var edges = [];

    for (var i = 0; i < containers.length; i++) {
        var container = containers[i];

        var details =
            "<b>Name:</b> " + container.Names[0] +
            "<br><b>Status:</b> " + container.Status +
            "<br><b>State:</b> " + container.State +
            "<br><b>Image:</b> " + container.Image;

        var node = {
            id: container.Id,
            label: container.Names[0],
            title: details
        };

        nodes.push(node);
    }

    for (var i = 0; i < networks.length; i++) {
        var network = networks[i];
        var containerIds = Object.keys(network.Containers);

        for (var j = 0; j < containerIds.length; j++) {
            var containerId = containerIds[j];
            
            for (var k = j + 1; k < containerIds.length; k++) {
                var edge = {
                    from: containerIds[j],
                    to: containerIds[k],
                    label: network.Name,
                    font: {
                            size: 9,
                            align: 'bottom',
                            color: 'gray',
                            strokeWidth: 0,
                        }
                };
                
                if(network.Name != 'bridge') {
                    edges.push(edge);
                }
            }
        }
    }
    
    return {
        nodes: nodes,
        edges: edges
    };
}

function refresh() {
    $.ajax({
        type: 'GET',
        url: "/data",
        dataType: 'json',
        async: true,
        success: function (data) {
            var network = processResponse(data);
            window.network.setData(network);
        }
    });
}

$(function () {
    var options = {
        physics: {
            stabilization: false
        },
        nodes: {
            shape: 'dot',
            borderWidth: 2,
            font: {
                color: 'white'
            }
        },
        edges: {
            width: 2,
            color: {
                inherit: 'both'
            }
        }
    };
    
    var container = $('#network').get(0);
    window.network = new vis.Network(container, { nodes: [], edges: [] }, options);

    refresh();

    // Refreshing instances every 1 minute
    window.setInterval(function () {
        refresh();
    }, 60 * 1000);

    // Reloading whole page every 30 minutes to avoid memory leaks in visjs
    // window.setInterval(function () {
    //     window.location.reload(true);
    // }, 60 * 1000 * 30);
});