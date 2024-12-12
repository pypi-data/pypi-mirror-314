const QuickChartPlugin = (function() {
    let initialized = false;
    let sourceData = null;
    let columns = {};
    let params = {x: '', y: [], y2: [], type: 'line', stack: false, cat_x: false, labels: false, agg: '', log_y: false};
    let chart = null;
    let apexPalette = 'palette7';
    let help = {
        'line': 'To build a line chart, select X and at least one of Y or Y2.',
        'bar': 'To build a bar chart, select X and at least one of Y or Y2.',
        'scatter': 'To build a scatter chart, select X and at least one of Y or Y2.',
        'area': 'To build a area chart, select X and at least one of Y or Y2.',
        'pie': 'To build a pie chart, select X and one and only one of Y.',
    }

    function appendQueryString(url, qs) {
        const op = url.includes('?') ? '&' : '?';
        return url+op+qs;
    }

    async function fetchData() {
        const jsonUrl = document.querySelector('link[rel="alternate"][type="application/json+datasette"]').href;
        const dataUrl = appendQueryString(jsonUrl, '_shape=array&_size=max');
        const resp = await fetch(dataUrl);
        sourceData = await resp.json();
        getColumns(sourceData);
    }

    function isValidChartType(chartType) {
        return ['line', 'area', 'bar', 'scatter', 'pie'].includes(chartType);
    }

    function loadParams() {
        const jsonString = sessionStorage.getItem('datasette-quickchart-params');
        let data = {};
        if (jsonString) {
            try {
                data = JSON.parse(jsonString);
            } catch {
                data = {};
            }
        }
        params.x = columns[data.x] ? data.x : '';
        for (const par of ['y', 'y2']) {
            const cols = data[par] || [];
            params[par] = cols.filter(col => columns.hasOwnProperty(col));
        }
        params.type = isValidChartType(data.type) ? data.type : 'line';
        params.stack = data.stack || false;
        params.cat_x = data.cat_x || false;
        params.labels = data.labels || false;
        params.agg = data.agg || '';
        params.log = data.log || false;
        //params.open = data.open || false;
    }

    function setPalette() {
        if (typeof QUICKCHART_PALETTE !== 'undefined') {
            apexPalette = `palette${QUICKCHART_PALETTE}`;
        }
    }

    function saveParams() {
        sessionStorage.setItem('datasette-quickchart-params', JSON.stringify(params));
    }

    function updateParams() {
        const tracesForm = document.getElementById('qc-traces');
        const traces = new FormData(tracesForm);
        params.x = traces.get('x') || '';
        for (const par of ['y', 'y2']) {
            params[par] = traces.getAll(par);
        }
        const configForm = document.getElementById('qc-config');
        const formData = new FormData(configForm);
        params.type = formData.get('type');
        params.stack = formData.get('stack') == '1';
        params.cat_x = formData.get('cat_x') == '1';
        params.labels = formData.get('labels') == '1';
        params.agg = formData.get('agg');
        params.log_y = formData.get('log_y') == '1';
    }

    function getInput(name, type, value, checked, title='', group='', label='') {
        const checkedAttr = checked ? ' checked' : '';
        const groupAttr = group ? ` data-group="${group}"` : '';
        const titleAttr = label ? '' : ` title="${title}"`;
        let html =`<input name="${name}" type="${type}" value="${value}"${titleAttr}${groupAttr}${checkedAttr} />`;
        if (label) {
            html = `<label title="${title}">${html}<span>${label}</span></label>`;
        }
        return html;
    }

    function radio(name, value, checked, title='', group='', label='') {
        return getInput(name, 'radio', value, checked, title, group, label);
    }

    function checkbox(name, value, checked, title='', group='', label='') {
        return getInput(name, 'checkbox', value, checked, title, group, label);
    }

    function td(html) {
        return `<td>${html}</td>`;
    }

    function ucfirst(s) {
        return s.charAt(0).toUpperCase() + s.substring(1);
    }

    function typeName(type) {
        return (type == 'time') ? 'Date/Time' : ucfirst(type);
    }

    function getTracesForm() {
        var html = '<table>';
        html += '<tr><th>Column</th><th>X</th><th>Y</th><th>Y2</th><th>Axis type</th></tr>';
        for (const [name, type] of Object.entries(columns)) {
            html += '<tr>' + td(name);
            html += td((type == 'null') ? '' : radio('x', name, name==params.x, '', name));
            if (type == 'numeric') {
                html += td(checkbox('y', name, params.y.includes(name), '', name));
                html += td(checkbox('y2', name, params.y2.includes(name), '', name));
            } else {
                html += '<td></td><td></td>';
            }
            html += td(typeName(type)) + '</tr>';
        }
        html += '</table>';
        return html;
    }

    function getConfigForm() {
        var html = '<div>';
        html += radio('type', 'line', params.type=='line', '', '', 'Line');
        html += radio('type', 'scatter', params.type=='scatter', '', '', 'Scatter');
        html += radio('type', 'area', params.type=='area', '', '', 'Area');
        html += radio('type', 'bar', params.type=='bar', '', '', 'Bar');
        html += radio('type', 'pie', params.type=='pie', '', '', 'Pie');
        html += '</div><div>'
        html += checkbox('labels', 1, params.labels, 'Show data labels', '', 'Labels');
        html += checkbox('stack', 1, params.stack, 'Stacked chart', '', 'Stacked');
        html += checkbox('cat_x', 1, params.cat_x, 'Treat X data as labels', '', 'Categ. X');
        //html += checkbox('log_y', 1, params.log_y, 'Logarithmic Y', '', 'Log');
        html += '</div><div id="qt-agg"><div>Agg:</div>';
        html += radio('agg', '', params.agg=='', 'Do not aggregate by X', 'agg', 'None');
        html += radio('agg', 'sum', params.agg=='sum', 'Sum by X', 'agg', 'Sum');
        html += radio('agg', 'avg', params.agg=='avg', 'Average by X', 'agg', 'Avg');
        html += '</div>';
        return html;
    }

    function setConfigFormDataset() {
        const form = document.getElementById('qc-config');
        form.dataset.chartType = params.type;
        form.dataset.xType = params.x ? columns[params.x] : '';
    }

    function isValidDate(val) {
        return Date.parse(val) > 0;
    }

    function valType(val) {
        const t = typeof val;
        if (t == 'number') {
            return 'numeric';
        } else if (t == 'string') {
            return isValidDate(val) ? 'time' : 'categorical';
        }
        return 'null';
    }

    function getColumns(data) {
        for (const row of data) {
            for (const [key, val] of Object.entries(row)) {
                const newType = valType(val);
                if (key in columns) {
                    const oldType = columns[key];
                    if ((newType != oldType) && (newType != 'null') && (oldType != 'categorical')) {
                        columns[key] = (oldType == 'null') ? newType : 'categorical';
                    }
                } else {
                    columns[key] = newType;
                }
            }
        }
    }

    function isStackable() {
        return (params.type == 'bar') && ((params.y.length > 1) || (params.y2.length > 1));
    }

    function getContent() {
        var html = '<div id="qc-left">';
        html += '<form id="qc-traces">' + getTracesForm() + '</form>';
        html += '<div id="qc-close"><a href="#">Close Quick Chart</a></div>';
        html += '</div>';
        html += '<div id="qc-right">';
        html += '<form id="qc-config">' + getConfigForm() + '</form>';
        html += '<div id="qc-chart"></div>'
        html += '</div>';
        return html;
    }

    function handleGroupedInputs(ev) {
        const target = ev.target;
        if (target.checked && target.dataset.group) {
            const group = target.dataset.group;
            const form = target.form;
            const inputs = form.querySelectorAll(`input[data-group="${group}"]`);
            for (const input of inputs) {
                if (input !== target) {
                    input.checked = false;
                }
            }
        }
    }

    function addEventListeners() {
        const tracesForm = document.getElementById('qc-traces');
        const configForm = document.getElementById('qc-config');
        for (const form of [tracesForm, configForm]) {
            const groupedInputs = form.querySelectorAll('input[data-group]');
            for (const input of groupedInputs) {
                input.addEventListener('change', handleGroupedInputs);
            }
            form.addEventListener('change', (ev) => {
                updateParams();
                setConfigFormDataset();
                saveParams();
                updateChart();
            });
        }
        document.querySelector('#qc-close a').addEventListener('click', (ev) => {
            ev.preventDefault();
            document.getElementById('qc-section').classList.remove('open');
            //params.open = false;
        });
    }

    function chartMessage(text) {
        const node = document.getElementById('qc-chart');
        node.innerHTML = text;
    }

    function readyToPlot() {
        if (params.x == '') {
            return false;
        }
        if (params.type.includes('pie')) {
            return (params.y.length == 1) && (params.y2.length == 0);
        }
        return (params.y.length > 0) || (params.y2.length > 0);
    }

    function allInt(data, col) {
        for (row of data) {
            if (!Number.isInteger) {
                return false;
            }
        }
        return true;
    }

    function subset(data, cols) {
        const result = [];
        for (const row of data) {
            const obj = {};
            for (const col of cols) {
                obj[col] = row[col];
            }
            result.push(obj);
        }
        return result;
    }

    function sortBy(data, by) {
        if (columns[by] === 'time') {
            return data.toSorted((a, b) => a[by] > b[by] ? 1 : -1);
        }
        return data.toSorted((a, b) => a[by] - b[by]);
    }

    function sum(values) {
        return values.reduce((acc, val) => acc + val, 0);
    }

    function absSum(values) {
        return values.reduce((acc, val) => acc + Math.abs(val), 0);
    }

    function mean(values) {
        const len = values.filter(el => el !== null).length;
        return len ? sum(values) / len : null;
    }

    function groupBy(data, by, aggFunc) {
        const grouped = new Map();
        for (const row of data) {
            const key = row[by];
            if (!grouped.has(key)) {
                grouped.set(key, {});
            }
            const group = grouped.get(key);
            for (const [field, value] of Object.entries(row)) {
                if (field != by) {
                    if (field in group) {
                        group[field].push(value);
                    } else {
                        group[field] = [value];
                    }
                }
            }
        }
        const result = [];
        for (const [key, fields] of grouped.entries()) {
            const row = {[by]: key};
            for (const [field, values] of Object.entries(fields)) {
                row[field] = aggFunc(values);
            }
            result.push(row);
        }
        return result;
    }

    function toApexType(colType) {
        return (colType == 'time') ? 'datetime' : (colType == 'numeric') ? 'numeric' : 'category';
    }

    function seriesName(colName, chartType, aggType) {
        let name = colName;
        if (chartType != 'pie') {
            if (aggType == 'sum') {
                name = `sum(${name})`;
            } else if (aggType == 'avg') {
                name = `avg(${name})`;
            }
        }
        return name;
    }

    function isDebugMode() {
        const hash = window.location.hash;
        return hash.includes('quickchart-debug');
    }

    function getPrecision(num) {
        return parseFloat(num).toPrecision(12).replace(/0+$/, '').split('.')[1].length;
    }

    function getFormatter(data, cols, compact=true) {
        const formatters = {};
        const numCols = [];
        for (const col of cols) {
            if (columns[col] == 'numeric') {
                numCols.push(col);
            }
        }
        if (numCols.length > 0) {
            let allInt = true;
            let maxVal = 0;
            let maxPrecision = 1;
            for (const row of data) {
                for (const col of numCols) {
                    const num = row[col];
                    if (allInt && !Number.isInteger(num)) {
                        allInt = false;
                    }
                    maxVal = Math.max(maxVal, Math.abs(num));
                    maxPrecision = Math.max(maxPrecision, getPrecision(num));
                }
            }
            if ((maxVal >= 10000) && compact) {
                return (new Intl.NumberFormat('en-US', {notation: 'compact', compactDisplay: 'short'})).format;
            } else if (allInt) {
                return (new Intl.NumberFormat('en-US', {maximumFractionDigits: 0})).format;
            } else {
                return (new Intl.NumberFormat('en-US', {mininumFractionDigits: maxPrecision, maximumFractionDigits: maxPrecision})).format;
            }
        }
        return (val) => val;
    }

    function getApexFormatterFunc(data, cols, compact=true) {
        const formatters = [];
        for (const col of cols) {
            formatters.push(getFormatter(data, [col], compact));
        }
        return (val, opts) => formatters[opts.seriesIndex](val);
    }

    function yAxis(fmt, log, right=false) {
        return {
            labels: {
                formatter: fmt
            },
            //logarithmic: log,
            opposite: right
        };
    }

    function updateChart() {
        if (!readyToPlot()) {
            chartMessage(help[params.type]);
            return;
        }

        const options = {
            chart: {
                type: params.type,
                height: 'auto',
                stacked: params.stack,
                toolbar: {show: true},
                animations: {speed: 400}
            },
            dataLabels: {
                enabled: params.labels,
                style: {
                    fontWeight: 'normal'
                }
            },
            theme: {
                palette: apexPalette
            },
            tooltip: {y: {}},
            xaxis: {
                type: params.cat_x ? 'category' : toApexType(columns[params.x])
            },
            yaxis: []
        };
        if (params.type === 'pie') {
            const valCol = params.y[0];
            let data = subset(sourceData, [params.x, valCol]);
            data = groupBy(data, params.x, absSum);
            options.series = data.map(row => row[valCol]);
            options.labels = data.map(row => row[params.x]);
            options.xaxis.labels = {formatter: getFormatter(data, [params.x])};
            options.tooltip.y.formatter = getFormatter(data, params.y, false);
        } else {
            let data = sourceData;
            if (columns[params.x] != 'categorical') {
                data = sortBy(data, params.x);
            }
            data = subset(data, params.y.concat(params.x, params.y2));
            if (params.agg) {
                const aggFunc = (params.agg == 'avg') ? mean : sum;
                data = groupBy(data, params.x, aggFunc);
            }
            if (columns[params.x] == 'numeric') {
                options.xaxis.labels = {
                    formatter: getFormatter(data, [params.x])
                };
            };
            options.dataLabels.formatter = getApexFormatterFunc(data, params.y.concat(params.y2), true);
            options.tooltip.y.formatter = getApexFormatterFunc(data, params.y.concat(params.y2), false);
            if (params.y.length > 0) {
                options.yaxis.push(yAxis(getFormatter(data, params.y), params.log_y));
            }
            if (params.y2.length > 0) {
                options.yaxis.push(yAxis(getFormatter(data, params.y2), params.log_y, true));
            }
            options.xaxis.categories = data.map(row => row[params.x]);
            options.series = [];
            for (const y of params.y) {
                options.series.push({
                    name: seriesName(y, params.type, params.agg),
                    data: data.map(row => row[y]),
                    yaxis: 1
                });
            }
            for (const y2 of params.y2) {
                options.series.push({
                    name: seriesName(y2, params.type, params.agg),
                    data: data.map(row => row[y2]),
                    yaxis: 2
                });
            }
            if (options.yaxis.length > 1) {
                options.yaxis[0].title = {text: params.y.join(' | '), style: {fontWeight: 400}};
                options.yaxis[1].title = {text: params.y2.join(' | '), style: {fontWeight: 400}, rotate:90};
            }
        }
        if (isDebugMode()) {
            console.log(options);
        }
        if (chart != null) {
            chart.destroy();
        }
        const chartDiv = document.getElementById('qc-chart');
        chartDiv.innerHTML = '';
        chart = new ApexCharts(chartDiv, options);
        setTimeout(() => chart.render(), 0);
    }

    async function init() {
        const panel = document.getElementById('qc-panel');
        if (!initialized) {
            await fetchData();
            loadParams();
            panel.innerHTML = getContent();
            setConfigFormDataset();
            addEventListeners();
            setPalette();
            updateChart();
            initialized = true;
        }
        panel.parentElement.classList.add('open');
        //params.open = true;
    }

    // Public API
    return {
        init: init
    };
})();

document.addEventListener('DOMContentLoaded', () => {
    const createElementWithId = (tag, id) => {
        const el = document.createElement(tag);
        el.id = id;
        return el;
    };
    const header = document.querySelector('.page-header,h1');
    if (header) {
        const outer = createElementWithId('div', 'qc-section');
        const button = createElementWithId('button', 'qc-open');
        button.type = 'button';
        button.textContent = 'Quick Chart';
        button.onclick = () => QuickChartPlugin.init();
        const panel = createElementWithId('div', 'qc-panel');
        outer.append(button, panel);
        // insert after header
        header.parentNode.insertBefore(outer, header.nextSibling);
    }
});
