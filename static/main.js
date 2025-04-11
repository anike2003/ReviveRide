document.addEventListener("DOMContentLoaded", function () {
    // Notification Button Logic
    $(".btn-custom").click(function () {
        $(".btn-custom").removeClass("active");
        $(this).addClass("active");

        $(".notification-content").hide();

        const buttonId = $(this).attr("id");
        const contentMap = {
            primaryBtn: "#primaryContent",
            appointmentBtn: "#appointmentContent",
            statusBtn: "#statusContent",
            alertsBtn: "#alertsContent"
        };

        if (contentMap[buttonId]) {
            $(contentMap[buttonId]).fadeIn();
        }
    });

    // Map Initialization
    mapboxgl.accessToken = 'pk.eyJ1IjoiZGFsd2luLTIiLCJhIjoiY2xyand3ZGVxMDZtODJ0cXJ6bTVqbXd6YyJ9.i5yryBgzS9JwD1CJBkoznQ';

    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v12',
        center: [3.3792, 6.5244],
        zoom: 12
    });

    map.addControl(new mapboxgl.NavigationControl());

    const input = document.getElementById('search-input');

    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            const query = input.value.trim();
            if (!query) return;

            // Call Mapbox geocoding API
            fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(query)}.json?access_token=${mapboxgl.accessToken}`)
                .then(response => response.json())
                .then(data => {
                    if (data.features.length > 0) {
                        const result = data.features[0];
                        const [lng, lat] = result.center;

                        // Fly to location
                        map.flyTo({ center: [lng, lat], zoom: 14 });

                        // Add a marker
                        new mapboxgl.Marker()
                            .setLngLat([lng, lat])
                            .addTo(map);
                    } else {
                        alert('No results found');
                    }
                })
                .catch(err => {
                    console.error('Geocoding error:', err);
                    alert('Error fetching location');
                });
        }
    });



    // AI Chatbot Logic
    const chatBody = document.querySelector(".chat-body");
    const messageInput = document.querySelector(".message-input");
    const sendMessageButton = document.querySelector("#send-message");

    const API_KEY = "AIzaSyCYOQSVOVs1bbLWY03Mx4Emxkq3U5Bekvo";
    const API_URL = `https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key=${API_KEY}`;
    const userData = { message: null };

    const createMessageElement = (content, ...classes) => {
        const div = document.createElement("div");
        div.classList.add("d-flex", ...classes, "align-items-center", "mb-3");
        div.innerHTML = content;
        return div;
    };

    const generateBotResponse = async (incomingMessageDiv) => {
        const messageElement = incomingMessageDiv.querySelector(".message-text");
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{ role: "user", parts: [{ text: userData.message }] }]
            })
        };

        try {
            const response = await fetch(API_URL, requestOptions);
            const data = await response.json();
            if (!response.ok) throw new Error(data.error.message);

            const apiResponseText = data.candidates[0].content.parts[0].text.replace(/\*\*(.*?)\*\*/g, "$1").trim();
            messageElement.innerText = apiResponseText;
        } catch (error) {
            console.error("API Error:", error);
            messageElement.innerText = "Oops! Something went wrong.";
            messageElement.style.color = "#ff0000";
        } finally {
            incomingMessageDiv.classList.remove("thinking");
        }
    };

    const handleOutGoingMessage = (e) => {
        e.preventDefault();
        userData.message = messageInput.value.trim();
        if (!userData.message) return;

        messageInput.value = "";

        const outgoingContent = `<div class="me-2"><img src="img/testimonial-1.jpg" class="rounded-circle" width="50px"></div>
            <div class="p-3 bg-white border rounded-3 shadow-sm text-wrap message-text" style="max-width: 75%;">${userData.message}</div>`;
        const outGoingMessageDiv = createMessageElement(outgoingContent, "justify-content-end");
        chatBody.appendChild(outGoingMessageDiv);
        chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });

        setTimeout(() => {
            const incomingContent = `<div class="me-2"><img src="img/testimonial-2.jpg" class="rounded-circle" width="50px"></div>
                <div class="p-3 bg-white border rounded-3 shadow-sm text-wrap message-text" style="max-width: 75%;">
                    <div class="thinking-indicator d-flex gap-1">
                        <div class="dot bg-secondary rounded-circle" style="width: 8px; height: 8px;"></div>
                        <div class="dot bg-secondary rounded-circle" style="width: 8px; height: 8px;"></div>
                        <div class="dot bg-secondary rounded-circle" style="width: 8px; height: 8px;"></div>
                    </div>
                </div>`;
            const incomingMessageDiv = createMessageElement(incomingContent, "justify-content-start", "thinking");
            chatBody.appendChild(incomingMessageDiv);
            chatBody.scrollTo({ top: chatBody.scrollHeight, behavior: "smooth" });
            generateBotResponse(incomingMessageDiv);
        }, 600);
    };

    messageInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && messageInput.value.trim()) {
            handleOutGoingMessage(e);
        }
    });

    sendMessageButton.addEventListener("click", handleOutGoingMessage);
});

(function ($) {
    "use strict";

    setTimeout(function () {
        if ($('#spinner').length > 0) $('#spinner').removeClass('show');
    }, 1);

    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });

    $('.back-to-top').click(function () {
        $('html, body').animate({ scrollTop: 0 }, 1500, 'easeInOutExpo');
        return false;
    });

    $('.sidebar-toggler').click(function () {
        $('.sidebar, .content').toggleClass("open");
        return false;
    });

    $('.pg-bar').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, { offset: '80%' });

    $('#calender').datetimepicker({
        inline: true,
        format: 'L'
    });

    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        items: 1,
        dots: true,
        loop: true,
        nav: false
    });

    var ctx1 = document.getElementById("worldwide-sales")?.getContext("2d");
    if (ctx1) {
        new Chart(ctx1, {
            type: "line",
            data: {
                labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                datasets: [{
                    label: "Services Used",
                    data: [10, 20, 15, 25, 22, 38],
                    borderColor: "green",
                    backgroundColor: "rgba(0, 128, 0, 0.1)",
                    tension: 0.4,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    x: { title: { display: true } },
                    y: { title: { display: true }, beginAtZero: true }
                },
                plugins: {
                    legend: { display: true, position: "top" }
                }
            }
        });
    }

    const appointmentsCanvas = document.getElementById("appointmentsChart");
    if (appointmentsCanvas) {
        const ctx = appointmentsCanvas.getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Oil Change", "Car Wash", "Tire Rotation"],
                datasets: [{
                    label: "Upcoming Appointments",
                    data: [2, 3, 2],
                    backgroundColor: "rgba(255, 206, 86, 0.7)",
                    borderColor: "rgba(255, 206, 86, 1)",
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: "y",
                plugins: { tooltip: { enabled: true } },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: 3.5,
                        ticks: { stepSize: 0.5 }
                    }
                }
            }
        });
    }

    const chartCanvas = document.getElementById("salesChart");
    if (chartCanvas) {
        const ctx2 = chartCanvas.getContext('2d');
        new Chart(ctx2, {
            type: 'pie',
            data: {
                labels: ['Cleanliness', 'Service Speed', 'Staff Friendliness', 'Value for Money', 'Overall Experience'],
                datasets: [{
                    data: [3, 3, 3, 3, 3],
                    backgroundColor: [
                        '#f98e86',
                        '#91d095',
                        '#76c2f4',
                        '#ffda68',
                        '#c47dd0'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    }

})(jQuery);