/*******************************************************************************

    FUNCTIONS FOR RENDERING CHARTS AND FETCHING TAB DATA.

*******************************************************************************/

const charts = {}; // Global variable for caching parsed chart json data
const chartNames = ['timeline', 'secondary'];

function handleTabLoad(targetTab, forceDataReload = false) {
    if (targetTab.searchActive) {
        return;
    }
    const fetchUrl = targetTab.getAttribute('data-tab-content-url');
    const tabIdPrefix = targetTab.getAttribute('data-tab-id-prefix');

    let tabCharts = (charts[tabIdPrefix] ??= {});
    if (!forceDataReload) {
        assignTabJson(tabCharts, tabIdPrefix);
    }

    fetchData = fetchUrl !== null && (forceDataReload || Object.keys(tabCharts).length === 0);

    if (fetchData) {
        handleTabFetching(targetTab, tabCharts, tabIdPrefix);
    } else {
        targetTab.rendered = true;
        waitAndRenderCharts(targetTab, tabCharts, tabIdPrefix);
    }
}

function handleTabFetching(targetTab, tabCharts, tabIdPrefix) {
    targetTab.searchActive = true;
    targetTab.searchFailed = false;

    const tabContent = document.querySelector(targetTab.getAttribute('href'));
    const dataReloadButton = tabContent.querySelector('.tab-reload-btn');
    const chartTabContent = tabContent.querySelector('.chart-tab-content');

    dataReloadButton.classList.add('disabled');

    // set the tab icon to loading.
    setTabLoading(targetTab);

    fetch(targetTab.getAttribute('data-tab-content-url'), {
        headers: {
            'Accept': 'text/html'
        }
    }).then(async response => {
        chartTabContent.innerHTML = await response.text();

        if (!response.ok) {
            setTabError(targetTab);
            return;
        }

        assignTabJson(tabCharts, tabIdPrefix)

        waitAndRenderCharts(targetTab, tabCharts, tabIdPrefix);

        targetTab.rendered = true;
        targetTab.searchActive = false;
        setTabDefault(targetTab);
    }).catch(error => {
        console.error(error);
        showError(targetTab, chartTabContent);
    }).finally(() => {
        targetTab.searchActive = false;
        dataReloadButton.classList.remove('disabled');
    });
}

function assignTabJson(tabCharts, tabIdPrefix) {
    chartNames.forEach(chartName => {
        const chartDataScript = document.getElementById(`${tabIdPrefix}-${chartName}-chart-data`);
        if (chartDataScript) {
            // Assign chart json data stored in obtained <script> elements to appropriate place
            tabCharts[chartName] = JSON.parse(chartDataScript.textContent);
        }
    });
}

function waitForPaint() {
    // This method of yielding to the browser renderer works only semi-reliably,
    // but all the other methods I found, reliably didn't work.
    return new Promise((resolve) => {
        setTimeout(resolve, 250);
    });
}

function showError(targetTab, tabContent) {
    targetTab.searchFailed = true;
    tabContent.innerHTML = `
        <div class="alert alert-danger">
            <b class="alert-heading fw-bold">
                ${tabContent.getAttribute('data-text-error-occurred')}
            </b>
        </div>
    `;
    setTabError(targetTab);
}

function setTabLoading(tab) {
    tab.querySelector('.tab-tag').innerHTML = `
        <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        <span class="visually-hidden">Loading...</span>
    `;
}

function setTabError(tab) {
    tab.querySelector('.tab-tag').innerHTML = `
        <i class="fas fa-fw fa-exclamation-triangle text-danger" aria-hidden="true"></i>
    `;
}

function setTabDefault(tab) {
    tab.querySelector('.tab-tag').innerHTML = '#';
}

function addDownloadLinks(chartId, chartElem) {
    addSVGDownloadLink(chartId, chartElem);
    addJSONDownloadLink(chartId);
    addCSVDownloadLink(chartId);
}

function downloadDataAsFile(dataUrl, filename) {
    const downloadLink = document.createElement('a');
    downloadLink.href = dataUrl;
    downloadLink.download = filename;
    downloadLink.click();
}

function addSVGDownloadLink(chartId, chartElem) {
    document.getElementById(`${chartId}_export_svg`).addEventListener('click', () => {
        const legendStatus = chartElem.layout.showlegend;
        Plotly.relayout(chartElem, {showlegend: true}); // Show legend for export

        Plotly.toImage(chartElem, {
            format: 'svg',
            height: chartElem.offsetHeight,
            width: chartElem.offsetWidth
        }).then((dataUrl) => {
            const filename = `${chartId}_export.svg`;
            downloadDataAsFile(dataUrl, filename);
        }).finally(() => {
            Plotly.relayout(chartElem, {showlegend: legendStatus}); // Restore legend
        });
    });
}

function addJSONDownloadLink(chartId) {
    document.getElementById(`${chartId}_export_json`).addEventListener('click', () => {
        const jsonDataScript = document.getElementById(`${chartId}-json-data`);
        const blob = new Blob([jsonDataScript.textContent], {type: 'application/json'});
        const dataUrl = window.URL.createObjectURL(blob);
        const filename = `${chartId}_export.json`;
        downloadDataAsFile(dataUrl, filename);
    });
}

function getCSVFromJSON(jsonData) {
    if (jsonData.length === 0) {
        return '';
    }

    const columnDelimiter = ',';
    const lineDelimiter = '\n';

    const keys = Object.keys(jsonData[0]);
    const csvHeader = keys.join(columnDelimiter);
    const csvData = jsonData
        .map(row => keys.map(key => row[key]).join(columnDelimiter))
        .join(lineDelimiter);

    return `${csvHeader}${lineDelimiter}${csvData}`;
}

function addCSVDownloadLink(chartId) {
    document.getElementById(`${chartId}_export_csv`).addEventListener('click', () => {
        const jsonDataScript = document.getElementById(`${chartId}-json-data`);
        const jsonData = JSON.parse(jsonDataScript.textContent);
        const csvData = getCSVFromJSON(jsonData);
        const blob = new Blob([csvData], {type: 'text/csv'});
        const dataUrl = window.URL.createObjectURL(blob);
        const filename = `${chartId}_export.csv`;
        downloadDataAsFile(dataUrl, filename);
    });
}

function renderCharts(tabCharts, tabIdPrefix) {
    chartNames.forEach(chartName => {
        if (tabCharts[chartName] !== undefined) {
            const chartId = `${tabIdPrefix}-${chartName}`;
            const chartElem = document.getElementById(chartId);
            Plotly.react(chartElem, tabCharts[chartName]).then(() => {
                const loadingElem = Array.from(chartElem.getElementsByClassName('loading'));
                loadingElem.forEach(le => {
                    chartElem.removeChild(le);
                });
            });
            addDownloadLinks(chartId, chartElem);
        }
    });
}

// Only render charts when the tab is active
function waitAndRenderCharts(tab, tabCharts, tabIdPrefix) {
    if (tab.classList.contains('active')) {
        renderCharts(tabCharts, tabIdPrefix);
    } else {
        tab.addEventListener('shown.bs.tab', () => {
            waitForPaint().then(() => {
                renderCharts(tabCharts, tabIdPrefix);
            });
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Select all active tabs, which are not ancestors of other, non-active tabs. (i.e., They are visible at page load)
    const visibleTabs = document.querySelectorAll('a.chart-tab.active:not(.tab-pane:not(.active) a.chart-tab.active)')
    visibleTabs.forEach(handleTabLoad);

    // If there are any non-active tabs of tabs, set up event listeners to render any ancestors which should be active.
    document.querySelectorAll('a.super-chart-tab:not(.active)').forEach(scht => {
        const targetSupertab = document.querySelector(scht.getAttribute('href'));
        scht.addEventListener('shown.bs.tab', () => {
            const activeSubtabs = targetSupertab.querySelectorAll('a.chart-tab.active');
            activeSubtabs.forEach(handleTabLoad);
        });
    });

    // Add event listeners for the rest of the tabs.
    document.querySelectorAll('a.chart-tab').forEach(
        cht => cht.addEventListener('show.bs.tab', (event) => {
            if (event.target.rendered || event.target.searchFailed) {
                return;
            }
            handleTabLoad(event.target);
        })
    );

    // In case there are reload buttons, set up event listeners for them.
    document.querySelectorAll('.tab-reload-btn').forEach(
        trb => trb.addEventListener('click', (event) => {
            const targetTabId = event.currentTarget.getAttribute('data-target-tab-id');
            const targetTab = document.getElementById(targetTabId);
            handleTabLoad(targetTab, true);
        })
    );
});
