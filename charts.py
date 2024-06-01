#conversationsData is loaded from your conversations.json file
const conversationsData = {
    
        "L8094": {
          "meta": {
            "movie_name": "A Nightmare on Elm Street 4: The Dream Master",
            "release_year": "1988",
            "rating": "5.20",
            "votes": "13590",
            "genre": ["fantasy", "horror", "thriller"]
          },
          "vectors": []
        },
        "L1234": {
          "meta": {
            "movie_name": "Inception",
            "release_year": "2010",
            "rating": "8.8",
            "votes": "1983220",
            "genre": ["action", "adventure", "sci-fi"]
          },
          "vectors": []
        },
        "L5678": {
          "meta": {
            "movie_name": "The Shawshank Redemption",
            "release_year": "1994",
            "rating": "9.3",
            "votes": "2456789",
            "genre": ["drama"]
          },
          "vectors": []
        },
        "L9876": {
          "meta": {
            "movie_name": "The Dark Knight",
            "release_year": "2008",
            "rating": "9.0",
            "votes": "2345678",
            "genre": ["action", "crime", "drama"]
          },
          "vectors": []
        },
        "L4321": {
          "meta": {
            "movie_name": "Pulp Fiction",
            "release_year": "1994",
            "rating": "8.9",
            "votes": "2123456",
            "genre": ["crime", "drama"]
          },
          "vectors": []
        },
        "L2468": {
          "meta": {
            "movie_name": "Forrest Gump",
            "release_year": "1994",
            "rating": "8.8",
            "votes": "1987654",
            "genre": ["drama", "romance"]
          },
          "vectors": []
        },
        "L1357": {
          "meta": {
            "movie_name": "Fight Club",
            "release_year": "1999",
            "rating": "8.8",
            "votes": "1876543",
            "genre": ["drama"]
          },
          "vectors": []
        },
        "L3690": {
          "meta": {
            "movie_name": "The Matrix",
            "release_year": "1999",
            "rating": "8.7",
            "votes": "1765432",
            "genre": ["action", "sci-fi"]
          },
          "vectors": []
        },
        "L2460": {
          "meta": {
            "movie_name": "The Godfather",
            "release_year": "1972",
            "rating": "9.2",
            "votes": "2654321",
            "genre": ["crime", "drama"]
          },
          "vectors": []
        },
        "L1350": {
          "meta": {
            "movie_name": "The Lord of the Rings: The Fellowship of the Ring",
            "release_year": "2001",
            "rating": "8.8",
            "votes": "1543210",
            "genre": ["action", "adventure", "drama"]
          },
          "vectors": []
        }
      };
      

// Extract nodes and links from the conversationsData
const nodes = Object.keys(conversationsData).map(key => ({ id: key, label: conversationsData[key].meta.movie_name }));
const links = [];

// Add links based on shared genres
Object.keys(conversationsData).forEach(sourceKey => {
    Object.keys(conversationsData).forEach(targetKey => {
        if (sourceKey !== targetKey) {
            const sourceGenres = conversationsData[sourceKey].meta.genre;
            const targetGenres = conversationsData[targetKey].meta.genre;
            const commonGenres = sourceGenres.filter(genre => targetGenres.includes(genre));

            if (commonGenres.length > 0) {
                links.push({ source: sourceKey, target: targetKey, commonGenres });
            }
        }
    });
});

// Create SVG container dimensions for the force-directed graph
const width = 800;
const height = 600;

// Create SVG container for the force-directed graph
const svg = d3.select('#graph-container')
    .append('svg')
    .attr('width', width)
    .attr('height', height);

// Create force simulation
const simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id))
    .force('charge', d3.forceManyBody())
    .force('center', d3.forceCenter(width / 2, height / 2));

// Create links
const link = svg.selectAll('line')
    .data(links)
    .enter().append('line')
    .style('stroke', '#999')
    .style('stroke-width', d => Math.sqrt(d.commonGenres.length));

// Create nodes
const node = svg.selectAll('circle')
    .data(nodes)
    .enter().append('circle')
    .attr('r', 10)
    .attr('fill', getRandomColor())
    .call(d3.drag()
        .on('start', dragStarted)
        .on('drag', dragged)
        .on('end', dragEnded))
    .on('mouseover', handleMouseOver)
    .on('mouseout', handleMouseOut);

// Create tooltips
const tooltip = d3.select('body').append('div')
    .attr('class', 'tooltip')
    .style('opacity', 0);

// Update positions on tick
simulation.on('tick', () => {
    link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

    node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
});

// Drag functions
function dragStarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
}

function dragEnded(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

// Tooltip functions
function handleMouseOver(event, d) {
    tooltip.transition()
        .duration(200)
        .style('opacity', 0.9);
    tooltip.html(d.label)
        .style('left', (event.pageX + 5) + 'px')
        .style('top', (event.pageY - 18) + 'px');
}

function handleMouseOut() {
    tooltip.transition()
        .duration(500)
        .style('opacity', 0);
}

// Function to generate random color
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Add interactivity features
// Highlight and show movie details on click
node.on('click', handleNodeClick);

// Zooming functionality
svg.call(d3.zoom().on('zoom', handleZoom));
// Function to handle node click
function handleNodeClick(event, d) {
    // Check if 'd' is defined and 'conversationsData' has the corresponding data
    if (d && d.id && conversationsData[d.id]) {
        // Reset styles for all nodes and links
        node.attr('stroke', null).attr('stroke-width', null);
        link.style('stroke', '#999').style('stroke-width', d => Math.sqrt(d.commonGenres.length));

        // Highlight clicked node and its links
        d3.select(this).attr('stroke', 'black').attr('stroke-width', 2);
        svg.selectAll('line').filter(link => link.source === d || link.target === d)
            .style('stroke', 'black').style('stroke-width', 2);

        // Display movie details in the tooltip
        const movieDetails = `
            <strong>Movie Name:</strong> ${d.label}<br>
            <strong>Release Year:</strong> ${conversationsData[d.id].meta.release_year}<br>
            <strong>Rating:</strong> ${conversationsData[d.id].meta.rating}<br>
            <strong>Genre:</strong> ${conversationsData[d.id].meta.genre.join(', ')}
        `;

        tooltip.transition().duration(200).style('opacity', 0.9);
        tooltip.html(movieDetails)
            .style('left', (event.pageX + 5) + 'px')
            .style('top', (event.pageY - 18) + 'px');
    }
}


// Function to handle zoom
function handleZoom(event) {
    if (svg) {
        svg.attr('transform', event.transform);
    }
}
// Create SVG container for the bar chart
const barChartSvg = d3.select('#bar-chart-container')
    .append('svg')
    .attr('width', 600)
    .attr('height', 750);

// Extract data for the bar chart
const barChartData = Object.keys(conversationsData).map(key => parseFloat(conversationsData[key].meta.rating));

// Create a color scale for the bar chart
const colorScale = d3.scaleSequential(d3.interpolateViridis)
    .domain([d3.min(barChartData), d3.max(barChartData)]);
// Create bars for the bar chart with different colors
barChartSvg.selectAll('rect')
    .data(barChartData)
    .enter().append('rect')
    .attr('x', (d, i) => i * 80)
    .attr('y', d => 300 - (d * 20)) // Adjust the scaling factor as needed
    .attr('width', 70)
    .attr('height', d => d * 20) // Adjust the scaling factor as needed
    .attr('fill', (d, i) => getLegendColor(conversationsData[Object.keys(conversationsData)[i]].meta.genre[0]));

// Create legend for the bar chart
const barLegend = barChartSvg.append('g')
    .attr('transform', 'translate(0,20)'); // Adjust the position of the legend

const legendData = ['fantasy', 'horror', 'thriller', 'action', 'adventure', 'sci-fi', 'drama', 'crime', 'romance'];

barLegend.selectAll('rect')
    .data(legendData)
    .enter().append('rect')
    .attr('x', (d, i) => i * 80)
    .attr('y', 0)
    .attr('width', 10)
    .attr('height', 10)
    .attr('fill', (d, i) => getLegendColor(d));

barLegend.selectAll('text')
    .data(legendData)
    .enter().append('text')
    .attr('x', (d, i) => i * 80 + 15)
    .attr('y', 9)
    .text(d => d);

// Function to get color for legend based on genre
function getLegendColor(genre) {
    const colorMap = {
        'fantasy': 'red',
        'horror': 'green',
        'thriller': 'blue',
        'action': 'orange',
        'adventure': 'purple',
        'sci-fi': 'brown',
        'drama': 'pink',
        'crime': 'gray',
        'romance': 'cyan'
    };
    return colorMap[genre] || 'black'; // Default to black if genre not found
}
// Optional: Add a title for the legend
barLegend.append('text')
    .attr('x', 10)
    .attr('y', -5)
    .attr('font-weight', 'bold')
    .text('Rating Legend');
    
barLegend.selectAll('rect')
    .data(['Bar Chart'])
    .enter().append('rect')
    .attr('x', 10)
    .attr('y', (d, i) => i * 20)
    .attr('width', 10)
    .attr('height', 10)
    .attr('fill', 'blue');


// Create SVG container for the pie chart
const pieChartSvg = d3.select('#pie-chart-container')
    .append('svg')
    .attr('width', 800)
    .attr('height', 800);

// Extract data for the pie chart
const pieChartData = Object.keys(conversationsData).map(key => parseFloat(conversationsData[key].meta.votes));

// Create pie chart in the middle with a full radius
const pie = d3.pie();
const arc = d3.arc().innerRadius(0).outerRadius(400); // Set outerRadius to 400 for a full pie

pieChartSvg.append('g')
    .attr('transform', 'translate(400,400)') // Center the pie chart
    .selectAll('path')
    .data(pie(pieChartData))
    .enter().append('path')
    .attr('d', arc)
    .attr('fill', (d, i) => d3.schemeCategory10[i]);

// Create legend for the pie chart
const pieLegend = pieChartSvg.append('g')
    .attr('transform', 'translate(580,20)'); // Adjust the position of the legend

pieLegend.selectAll('rect')
    .data(pieChartData)
    .enter().append('rect')
    .attr('x', 10)
    .attr('y', (d, i) => i * 20)
    .attr('width', 10)
    .attr('height', 10)
    .attr('fill', (d, i) => d3.schemeCategory10[i]);

pieLegend.selectAll('text')
    .data(pieChartData)
    .enter().append('text')
    .attr('x', 25)
    .attr('y', (d, i) => i * 20 + 9)
    .text((d, i) => `Movie ${i + 1}`);


      // Conversations data from conversations.json
      const conversationsDataTree = {
        name: 'Movies',
        children: [
          {
            name: 'Fantasy',
            children: [
              {
                name: 'A Nightmare on Elm Street 4: The Dream Master',
                meta: {
                  movie_name: 'A Nightmare on Elm Street 4: The Dream Master',
                  release_year: '1988',
                  rating: '5.20',
                  votes: '13590',
                  genre: ['fantasy', 'horror', 'thriller'],
                },
              },
            ],
          },
          {
            name: 'Action',
            children: [
              {
                name: 'Inception',
                meta: {
                  movie_name: 'Inception',
                  release_year: '2010',
                  rating: '8.8',
                  votes: '1983220',
                  genre: ['action', 'adventure', 'sci-fi'],
                },
              },
              {
                name: 'The Dark Knight',
                meta: {
                  movie_name: 'The Dark Knight',
                  release_year: '2008',
                  rating: '9.0',
                  votes: '2345678',
                  genre: ['action', 'crime', 'drama'],
                },
              },
              {
                name: 'The Matrix',
                meta: {
                  movie_name: 'The Matrix',
                  release_year: '1999',
                  rating: '8.7',
                  votes: '1765432',
                  genre: ['action', 'sci-fi'],
                },
              },
              {
                name: 'The Lord of the Rings: The Fellowship of the Ring',
                meta: {
                  movie_name: 'The Lord of the Rings: The Fellowship of the Ring',
                  release_year: '2001',
                  rating: '8.8',
                  votes: '1543210',
                  genre: ['action', 'adventure', 'drama'],
                },
              },
            ],
          },
          {
            name: 'Drama',
            children: [
              {
                name: 'The Shawshank Redemption',
                meta: {
                  movie_name: 'The Shawshank Redemption',
                  release_year: '1994',
                  rating: '9.3',
                  votes: '2456789',
                  genre: ['drama'],
                },
              },
              {
                name: 'Pulp Fiction',
                meta: {
                  movie_name: 'Pulp Fiction',
                  release_year: '1994',
                  rating: '8.9',
                  votes: '2123456',
                  genre: ['crime', 'drama'],
                },
              },
              {
                name: 'Forrest Gump',
                meta: {
                  movie_name: 'Forrest Gump',
                  release_year: '1994',
                  rating: '8.8',
                  votes: '1987654',
                  genre: ['drama', 'romance'],
                },
              },
              {
                name: 'Fight Club',
                meta: {
                  movie_name: 'Fight Club',
                  release_year: '1999',
                  rating: '8.8',
                  votes: '1876543',
                  genre: ['drama'],
                },
              },
            ],
          },
          {
            name: 'Crime',
            children: [
              {
                name: 'The Godfather',
                meta: {
                  movie_name: 'The Godfather',
                  release_year: '1972',
                  rating: '9.2',
                  votes: '2654321',
                  genre: ['crime', 'drama'],
                },
              },
            ],
          },
        ],
      };
      
      const treeData = conversationsDataTree;

      // Create a tree layout
      const treeLayout = d3.tree().size([600, 400]);

      // Create a root node from the tree data
      const rootNode = d3.hierarchy(treeData);

      // Assign coordinates to each node in the tree
      treeLayout(rootNode);

      // Create SVG container for the tree chart
      const treeSvg = d3.select('#tree-container')
          .append('svg')
          .attr('width', 800)
          .attr('height', 600)
          .append('g')
          .attr('transform', 'translate(50,50)'); // Adjust as needed

      // Add links
      treeSvg.selectAll('path.link')
          .data(rootNode.links())
          .enter().append('path')
          .attr('class', 'link')
          .attr('d', d3.linkHorizontal()
              .x(d => d.y)
              .y(d => d.x)
          );

      // Add nodes
      const nodes1 = treeSvg.selectAll('g.node')
          .data(rootNode.descendants())
          .enter().append('g')
          .attr('class', 'node')
          .attr('transform', d => `translate(${d.y},${d.x})`);

      nodes1.append('circle')
          .attr('r', 7);

      nodes1.append('text')
          .attr('dy', 3)
          .attr('x', d => d.children ? -8 : 8)
          .attr('text-anchor', d => d.children ? 'end' : 'start')
          .text(d => d.data.name);