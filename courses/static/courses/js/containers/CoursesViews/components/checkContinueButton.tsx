import React from 'react'

import Button from '@material-ui/core/Button'
import { useTheme } from '@material-ui/core/styles'
import useMediaQuery from '@material-ui/core/useMediaQuery'

import UserStateEnum from '../const'

import {
  continueMessage,
  saveDataMessage,
  checkUserReactionMessage,
} from '../../../utils/iframe/postMessages'
import { checkSaveButtonStyle, checkSaveButtonStyleDisabled } from './style'

// eslint-disable-next-line @typescript-eslint/interface-name-prefix
interface CheckContinueProps {
  // currentMaterial: materialActionCreators.MaterialRedux
  currentMaterial: object
  editMode: boolean
  disabledCheck: boolean
  // userReactionState: string // todo enum?
  // TODO see src/models/material.ts in https://github.com/studyhub-co/components-library
  userReactionResult: any
}

const CheckContinueButton: React.FC<CheckContinueProps> = props => {
  const { currentMaterial, editMode, disabledCheck, userReactionResult } = props

  const theme = useTheme()
  const matchesWideScreen = useMediaQuery(theme.breakpoints.up('sm'))
  console.log(matchesWideScreen)

  return (
    <div style={{ textAlign: 'center' }}>
      {currentMaterial && editMode ? (
        <Button
          style={{
            width: matchesWideScreen ? '60%' : '90%',
            ...checkSaveButtonStyle,
          }}
          variant="contained"
          color="primary"
          onClick={saveDataMessage}
        >
          Save
        </Button>
      ) : (
        <Button
          disabled={disabledCheck}
          style={{
            width: matchesWideScreen ? '60%' : '90%',
            ...(disabledCheck
              ? checkSaveButtonStyleDisabled
              : checkSaveButtonStyle),
          }}
          variant="contained"
          color="primary"
          onClick={
            userReactionResult.state === 'start'
              ? checkUserReactionMessage
              : continueMessage
          }
        >
          {userReactionResult.state === UserStateEnum.start && 'Check'}
          {userReactionResult.state === UserStateEnum.checked && 'Continue'}
        </Button>
      )}
    </div>
  )
}

export default CheckContinueButton
