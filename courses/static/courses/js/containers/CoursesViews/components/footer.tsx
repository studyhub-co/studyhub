import React, { useState, useEffect } from 'react'

import Modal from 'react-bootstrap/Modal'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import ProgressBar from 'react-bootstrap/ProgressBar'
import Button from 'react-bootstrap/Button'

import { makeStyles } from '@material-ui/core/styles'
import ButtonUI from '@material-ui/core/Button'
import CloseIcon from '@material-ui/icons/Close'
// import ArrowForwardIosIcon from '@material-ui/icons/ArrowForwardIos'

import ThreadComponent from '@studyhub.co/react-comments-django-client/lib/ThreadComponent'

import history from '../../../history'

import CheckContinueButton from './checkContinueButton'
import { FaCheckCircle, FaTimesCircle } from 'react-icons/fa'
import UserStateEnum from '../const'
import { calculateProgress } from '../utils'
import { continueMessage } from '../../../utils/iframe/postMessages'

// fixme copied from studyhub components library, todo remove unnecessary code
interface FooterProps {
  // currentMaterial: materialActionCreators.MaterialRedux;
  currentMaterial: any
  editMode?: boolean
  disabledCheck: boolean
  // updateMaterial(material: Material): void;
  // moveToNextComponent(previousMaterialUuid: string): void;
  // checkUserMaterialReaction(material: Material): void;
  // componentData: IQAData | null; // Any component IData
  userReactionState: string // todo enum?
}

const useStyles = makeStyles(theme => ({
  skipButton: {
    backgroundColor: 'rgb(219, 219, 219)',
    borderColor: '#979797',
    color: '#4c4c4c',
    minWidth: 0,
    // padding: '0.5rem 2rem',
    borderRadius: '12rem',
  },
  exitButton: {
    borderRadius: '12rem',
  },
}))

const Footer: React.FC<FooterProps> = props => {
  const {
    currentMaterial,
    editMode,
    // disabledCheck,
    // updateMaterial,
    // checkUserMaterialReaction,
    // componentData,
    // userReactionState
    // moveToNextComponent
  } = props

  const classes = useStyles()

  const [showCommentsModal, setShowCommentsModal] = useState(false)

  // data: {
  //   state: 'checked',
  //   user_lesson_score: 20,
  //   was_correct: true,
  // },
  const [userReactionResult, setUserReactionResult] = useState({
    state: UserStateEnum.start,
    userLessonScore: undefined,
    wasCorrect: undefined,
  })

  const [disabledCheck, setDisabledCheck] = useState(true)

  const handleShowComments = (): void => {
    setShowCommentsModal(!showCommentsModal)
  }

  useEffect(() => {
    const messageListener = ({ data }) => {
      if (data.hasOwnProperty('type')) {
        // disabled_check_button received from iframe
        if (data.type === 'disabled_check_button') {
          setDisabledCheck(data.data)
        }
        // user reaction state
        if (data.type === 'user_reaction_state') {
          setUserReactionResult(data.data)
          setPercentCompleted(
            calculateProgress(
              data.data.userLessonScore,
              currentMaterial.lesson?.complete_boundary,
            ),
          )
          // data: {
          //   state: 'checked',
          //   userLessonScore: 20,
          //   wasCorrect: true,
          // },
        }
      }
    }

    window.addEventListener('message', messageListener, false)
    return () => window.removeEventListener('message', messageListener)
  }, [])

  let backgroundColor = '#dbdbdb'
  let reactionResultIcon = (
    <FaCheckCircle
      id="correct"
      className="pull-right"
      style={{ fontSize: '35px' }}
    />
  )
  let correctMessage = 'Correct'

  if (userReactionResult.wasCorrect === false) {
    reactionResultIcon = (
      <FaTimesCircle
        id="incorrect"
        className="pull-right"
        style={{ fontSize: '35px' }}
      />
    )
    backgroundColor = '#ffd3d1'
    correctMessage = 'Incorrect'
  } else if (userReactionResult.wasCorrect === true) {
    backgroundColor = '#bff199'
  }

  // calculate with ratio
  const [percentCompleted, setPercentCompleted] = useState(
    calculateProgress(currentMaterial?.lesson_progress || 0),
  )

  const commentsModal = (
    <Modal
      show={showCommentsModal}
      onHide={handleShowComments}
      dialogClassName="modal-90w"
      aria-labelledby="example-custom-modal-styling-title"
    >
      <Modal.Header closeButton>
        <Modal.Title id="example-custom-modal-styling-title">
          Discussion
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {/*{this.props.solutionText &&*/}
        {/*    <MarkdownMathRender source={this.props.solutionText} />*/}
        {/*}*/}
        {/* TODO we can't show correct answer here */}
        {/*{correctAnswer}*/}
        <ThreadComponent
          anonAsUserObject={Boolean(true)}
          threadId={currentMaterial.thread}
        />
      </Modal.Body>
    </Modal>
  )

  return (
    <div
      id="footer"
      style={{
        backgroundColor: backgroundColor,
        // padding: '1rem 0 0 0',
        // fixme do we need this?
        // position: window.IS_IOS && window.IS_MOBILE_APP ? 'relative' : 'fixed',
      }}
    >
      <Container fluid>
        {userReactionResult.state === UserStateEnum.checked ? (
          <Row
            className="justify-content-md-center"
            style={{ padding: '0.5rem' }}
          >
            <Col
              xs={6}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                // paddingBottom: '0.5rem',
              }}
            >
              {reactionResultIcon}
              <span style={{ marginLeft: '0.5rem' }}>{correctMessage}</span>
            </Col>
            <Col
              xs={6}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <Button
                onClick={handleShowComments}
                style={{
                  backgroundColor: '#8d33d9',
                  borderColor: '#8d33d9',
                  borderBottomColor: '#8d33d9',
                  // padding: '0.5rem 2rem',
                  borderRadius: '12rem',
                }}
              >
                Comments
              </Button>
            </Col>
          </Row>
        ) : null}
        {commentsModal}
        <Row style={{ padding: '2vh 0' }}>
          <Col
            style={{
              display: 'flex',
              alignItems: 'center',
              flexWrap: 'nowrap',
              justifyContent: 'space-between',
              padding: '0 2rem',
            }}
          >
            <div style={{ flexShrink: 2, flexGrow: 0 }}>
              <ButtonUI
                title={'Exit'}
                variant="text"
                onClick={e => {
                  e.preventDefault()
                  history.push(
                    `/courses/modules/${currentMaterial.lesson.module}`,
                  )
                }}
                className={classes.exitButton}
              >
                <CloseIcon />
              </ButtonUI>
            </div>
            <div style={{ flexGrow: 6 }}>
              <CheckContinueButton
                // moveToNextComponent={moveToNextComponent}
                editMode={editMode ? true : false}
                // componentData={componentData}
                // checkUserMaterialReaction={checkUserMaterialReaction}
                currentMaterial={currentMaterial}
                disabledCheck={disabledCheck}
                // updateMaterial={updateMaterial}
                userReactionResult={userReactionResult}
              />
            </div>
            <div style={{ flexShrink: 2, flexGrow: 0 }}>
              {userReactionResult.state !== UserStateEnum.checked && (
                <ButtonUI
                  onClick={continueMessage}
                  title={'Skip'}
                  variant="contained"
                  className={classes.skipButton}
                >
                  Skip
                </ButtonUI>
              )}
            </div>
          </Col>
        </Row>
        <Row style={{ padding: '0 2vw 2vh 2vw' }}>
          <Col
          // style={{
          //   display: 'flex',
          //   alignItems: 'center',
          //   justifyContent: 'center',
          // }}
          >
            <ProgressBar
              style={{ height: '1rem' }}
              now={percentCompleted}
              // label={`${percentCompleted}%`}
            />
          </Col>
        </Row>
      </Container>
    </div>
  )
}

export default Footer
