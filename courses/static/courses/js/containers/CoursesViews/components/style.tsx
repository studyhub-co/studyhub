export const checkSaveButtonStyle = {
  borderRadius: '12rem',
  // border: '.2rem solid #1caff6',
  background: '#1caff6',
  color: '#fff',
  transition: 'color .5s,border .5s',
  outline: 'none',
  whiteSpace: 'nowrap',
  // width: '90%',
  // margin: '1rem 0 1rem 0', this should set in parent components
}

export const checkSaveButtonStyleDisabled = {
  ...checkSaveButtonStyle,
  background: 'gray',
  // border: '.2rem solid gray',
}
