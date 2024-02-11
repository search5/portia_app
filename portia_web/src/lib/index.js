const format_obj = new Intl.NumberFormat()
import axios from 'axios';

const http_inst = axios.create();

http_inst.interceptors.request.use(config => {
	// Do something before request is sent
	const accessToken = localStorage.getItem('access_token');
	// access 토큰을 가져오는 함수
	if (accessToken) {
		config.headers['Authorization'] = 'Bearer ' + accessToken;
	}

	return config;
},
(error) => {
	// Do something with request error
	return Promise.reject(error);
})

function number_format(value) {
  return format_obj.format(value)
}

function paginate({current, max}) {
	if (!current || !max) return null

	let prev = current === 1 ? null : current - 1,
			next = current === max ? null : current + 1,
			items = [1]

	if (current === 1 && max === 1) return {current, prev, next, items}
	if (current > 4) items.push('…')

	let r = 2, r1 = current - r, r2 = current + r

	for (let i = r1 > 2 ? r1 : 2; i <= Math.min(max, r2); i++) items.push(i)

	if (r2 + 1 < max) items.push('…')
	if (r2 < max) items.push(max)

	return {current, prev, next, items}
}

function isPositiveInteger(n) {
    return 0 === n % (!isNaN(parseFloat(n)) && 0 <= ~~n);
}

export { number_format, paginate, isPositiveInteger, http_inst }