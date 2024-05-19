import React from 'react'
import UltimateGridview from './UltimateGridview'
import VisionUserInterface from './VisionUserInterface'

const Vision = (props) => {
  return (
    <React.Fragment>Vision
      <VisionUserInterface />
      <UltimateGridview
        view_width={1000}
        view_height={600}
        world_width={300}
        world_height={300}
        defaultEnabled={true}
        experimentalFeaturesEnabled={true} />

    </React.Fragment>
  )
}

export default Vision;