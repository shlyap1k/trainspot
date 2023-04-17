function nextYear(date) {
  return (Number(date.split('-')[0])+1)+'-' + date.split('-').slice(1, 3).join('-')
}

export default nextYear
