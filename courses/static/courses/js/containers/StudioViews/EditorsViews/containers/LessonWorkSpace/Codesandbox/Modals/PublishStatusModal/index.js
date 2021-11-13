import React, { useEffect, useState } from 'react'
import { useOvermind } from '../../app/overmind'
import { api } from '../../app/overmind/effects'
import { Block } from '../MoveSandboxFolderModal/elements'
import { Container } from '../elements'
import { Button } from '@codesandbox/common/lib/components/Button'

function PublishStatusModal() {
  const {
    state: {
      editor: { currentSandbox: sandbox },
    },
    actions: { refetchSandboxInfo },
  } = useOvermind()

  // request
  const [loading, setLoading] = useState(false)
  const [publishStatus, setPublishStatus] = useState(sandbox.publishStatus)

  return (
    <div>
      <Block>Publishing status of &apos;{sandbox.title}&apos;</Block>
      <Container style={{ maxHeight: 400, overflow: 'auto' }}>
        {loading ? (
          'Requesting publishing status...'
        ) : (
          <div>
            <p>{publishStatus}</p>
            <Button
              // onClick={refetchSandboxInfo} -- overmind do not update sandbox here
              onClick={() => {
                ;(async sandbox => {
                  setLoading(true)
                  const sandbox1 = await api.getSandbox(sandbox.uuid)
                  setPublishStatus(sandbox1.publishStatus)
                  setLoading(false)
                })(sandbox)
                refetchSandboxInfo()
              }}
              style={{ display: 'inline-flex', alignItems: 'center' }}
              small
              disabled={loading}
            >
              Refresh status
            </Button>{' '}
            (Retry in 2-5 minutes)
          </div>
        )}
      </Container>
    </div>
  )
}

export default PublishStatusModal
