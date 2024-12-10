async function getActivities() {
	if (getActivities.calling)
		return;
	getActivities.calling = true;
	const e = document.getElementById("activities-list-div");
	e.replaceChildren();
	const activities = (await post("/chaoxing/get_activities")).json();
	if (!Object.keys(activities).length)
		e.innerText = "No ongoing activities.";
	for (let class_id in activities) {
		const course_activities = activities[class_id];
		e.appendChild(newElement("div", {
			innerText: class_id in globalThis.g_courses ?
				   `${globalThis.g_courses[class_id].name}: ` :
				   `${class_id}: `
		}));
		course_activities.forEach(a => {
			const type = a.type == "2" ? `Qrcode` : `Location`;
			const ts_a = a.time_start;
			const te_a = a.time_end || "????-??-?? ??:??";
			const ts_y = ts_a.slice(0, 4);
			const ts_md = ts_a.slice(5, 10);
			const ts_hm = ts_a.slice(11, 16);
			const te_y = te_a.slice(0, 4);
			const te_md = te_a.slice(5, 10);
			const te_hm = te_a.slice(11, 16);
			let ts = "", te = "";
			if (ts_y != te_y) {
				ts += `${ts_y}-`;
				te += `${te_y}-`;
			}
			if (ts_y != te_y || ts_md != te_md) {
				ts += `${ts_md} `;
				te += `${te_md} `;
			}
			ts += ts_hm;
			te += te_hm;
			const b = newElement("button", {
				disabled: a.type == "2",
				innerText: `${a.name} (${type}, ${ts} ~ ${te})`,
				onclick: () => chaoxingCheckinLocationWrapper(a)
			});
			e.appendChild(b);
		});
	}
	getActivities.calling = false;
}

async function chaoxingCheckinLocation(activity) {
	const res = await post("/chaoxing/checkin_checkin_location", {
		"location": globalThis.g_location, activity
	});
	const data = res.json();
	if (res.status != 200) {
		alert(`Checkin error. (Backend error, ${res.status})`);
		return;
	}
	alert(unescapeUnicode(data.msg));
}

async function chaoxingCheckinLocationWrapper(activity) {
	chaoxingCheckinLocation(activity);
}

async function chaoxingCheckinQrcode(url, result_div_id) {
	const e_id_prefix = result_div_id.split('-')[0];
	const data = {
		"location": globalThis.g_location, "video": "", "url": ""
	};
	if (globalThis.g_is_ios && e_id_prefix.startsWith("player"))
		data["video"] = globalThis.g_player_sources[
				 e_id_prefix.substring(e_id_prefix.length - 1)];
	else
		data["url"] = url;
	const res = await post("/chaoxing/checkin_checkin_qrcode_url", data);
	const d = res.json();
	document.getElementById(result_div_id).innerText =
						       unescapeUnicode(d.msg) ||
				`Checkin error. (Backend error, ${res.status})`;
	if (res.status != 200)
		return;
	if (d.msg.includes("success"))
		alert(unescapeUnicode(d.msg));
};

async function chaoxingCheckinQrcodeWrapper(video, result_div_id) {
	if (video.paused) {
		document.getElementById(result_div_id).innerText =
					     "Checkin error. (No image given.)";
		return;
	}
	try {
		if (globalThis.g_is_ios) {
			chaoxingCheckinQrcode("", result_div_id);
			return;
		}
		const urls = await screenshot_scan(video);
		if (!urls.length) {
			document.getElementById(result_div_id).innerText =
					 "Checkin error. (No Qrcode detected.)";
			return;
		}
		const curls = urls.filter(v => v.includes("widget/sign/e"));
		if (!curls.length) {
			document.getElementById(result_div_id).innerText =
				`Checkin error. (No checkin URL in [${urls}].)`;
			return;
		}
		for (let curl of curls)
			await chaoxingCheckinQrcode(curl, result_div_id);
	}
	catch (e) {
		document.getElementById(result_div_id).innerText =
						`Checkin error. (${e.message})`;
	}
}
