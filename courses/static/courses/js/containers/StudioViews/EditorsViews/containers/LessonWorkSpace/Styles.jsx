import React from 'react'

import styled from 'styled-components'

import { createTheme, ThemeProvider } from '@material-ui/core/styles'

export default function ThemeWraper(props) {
  const theme = React.useMemo(() =>
    createTheme({
      palette: {
        type: 'light',
      },
    }),
  )

  return <ThemeProvider theme={theme}>{props.children}</ThemeProvider>
}

export const StyledIframe = styled.iframe`
  border-width: 0;
  width: 100%;
  height: 100%;
  min-height: 0;
  overflow: auto;
`
