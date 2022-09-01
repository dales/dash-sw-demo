self.addEventListener("install", event => {
    console.log("Service worker installed 👍");
});

self.addEventListener("activate", event => {
    event.waitUntil(clients.claim());
    console.log("Service worker activated 👍");
});

async function remove_data_obj(initialRequest) {
    const request = await initialRequest.clone();
    const payload = await request.json();
    const VIEW_LIST_ID = "view-list";
    let views = (payload.state || []).filter(item => item.id === VIEW_LIST_ID);
    let prevViews = [];
    if (views.length > 0) {
        prevViews = views[0].value;
        views[0].value = prevViews.map(v => v.props.id.index);
    }
    const destURL = new URL(request.url);
    const headers = new Headers(request.headers);
    headers.append("A-SW", "Intercepted");

    response = await fetch(destURL, {
        method: request.method,
        headers,
        body: JSON.stringify(Object.assign(payload))
    });
    try {
        if (response.status !== 204) {
            let res_json = await response.json();
            if (prevViews.length > 0) {
                const views = res_json.response[VIEW_LIST_ID].children;
                // views[0].props.id.index = prevViews.length + 1;
                res_json.response[VIEW_LIST_ID].children = prevViews.concat(
                    views
                );
            }
            return new Response(JSON.stringify(res_json), {
                headers: response.headers
            });
        } else {
            let textResult = await response.text();
            console.warn(
                `Received 204 - text response: '${textResult}'. Creating an empty reponse`
            );
            return new Response(textResult || '{"response": {"props":{}}}', {
                headers: response.headers
            });
        }
    } catch (e) {
        console.log(e, response);
        return new Response({ headers: response.headers });
    }
}

self.addEventListener("fetch", function(event) {
    if (event.request.url.includes("_dash-update-component")) {
        return event.respondWith(remove_data_obj(event.request));
    }
});
