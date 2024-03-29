import React, { useState } from 'react'

// import DialogContentText from '@material-ui/core/DialogContentText'
import TextField from '@material-ui/core/TextField'
import Box from '@material-ui/core/Box'
// import Button from '@material-ui/core/Button'

interface ILogInProps {
  onDataChange(email: string, password: string): void
  setModalType(type: string): void
  loginIncorrectLogin?: boolean
}

export default function LogIn(props: ILogInProps) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const onChangeEmail = e => {
    setEmail(e.target.value)
    props.onDataChange(e.target.value, password)
  }

  const onChangePassword = e => {
    setPassword(e.target.value)
    props.onDataChange(email, e.target.value)
  }

  return (
    <React.Fragment>
      <TextField
        error={props.loginIncorrectLogin}
        helperText={
          'The e-mail address and/or password you specified are not correct.'
        }
        autoFocus
        variant="outlined"
        margin="dense"
        name="login"
        autoComplete="login"
        value={email}
        id="id_login"
        label="Email Address"
        placeholder={'Email'}
        type="email"
        onChange={onChangeEmail}
        fullWidth
      />
      <Box display="flex" alignItems="center">
        <Box flexGrow={1}></Box>
        <Box>
          <a
            className="navlink"
            style={{ cursor: 'pointer' }}
            onClick={() => {
              props.setModalType('passwordReset')
            }}
          >
            Forgot password?
          </a>
        </Box>
      </Box>
      <TextField
        error={props.loginIncorrectLogin}
        value={password}
        variant="outlined"
        onChange={onChangePassword}
        autoFocus
        margin="dense"
        autoComplete="password"
        name="password"
        id="id_password"
        label="Password"
        placeholder={'Password'}
        type="password"
        fullWidth
      />
    </React.Fragment>
  )
}
