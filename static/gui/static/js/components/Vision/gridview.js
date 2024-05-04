import React, { useEffect, useState } from "react";
import axios from "axios";

import { TransformWrapper, TransformComponent } from "react-zoom-pan-pinch";
import { withCookies } from "react-cookie";
import Vector from "./CollisionDetection/Vector";
import { logIfShapesCollide } from "./CollisionDetection/CollisionDection";


const scaleFactor = 40;
const distanceBetweenTicks = 10;

const widthPadding = 200;
const heightPadding = 50;
const botWidth = 5;
const botLength = 5;
const botHeight = 5;
const unknownMeasure = 2.5;
const unknownColor = "black";

/**
 * Component for the grid view of the simulated bots.
 */
const GridView = (props) => {

  const [displayIntervalId, setDisplayIntervalId] = useState(null);
  const [collisionIntervalId, setCollisionIntervalId] = useState(null);
  const [detections, setDetections] = useState([]);
  const [displayOn, setDisplayOn] = useState(false);
  const [virtualRoomId, setVirtualRoomId] = useState(props.cookies.get('virtual_room_id'));
  useEffect(() => {
    setVirtualRoomId(props.cookies.get('virtual_room_id'));
  }, [document.cookie]);

  useEffect(() => {
    if (displayOn) {
      clearInterval(displayIntervalId);
      clearInterval(collisionIntervalId);
      setDetections([]);
      setDisplayIntervalId(setInterval(getVisionData, 100));
      setCollisionIntervalId(setInterval(checkCollisions, 100));
    }
  }, [virtualRoomId]);

  useEffect(() => {
    if (displayOn) {
      clearInterval(collisionIntervalId);
      if (detections && detections.length > 1) {
        logIfShapesCollide(detections);
        // setCollisionIntervalId(setInterval(checkCollisions, 100));
      }
    }
  }, [detections]);



  /**
   * Executes after the component gets rendered.
   **/
  useEffect(() => {
    if (props.defaultEnabled) {
      toggleVisionDisplay();
    }
    return () => {
      // Anything in here is fired on component unmount.
      clearInterval(find);
    }
  }, []);


  const renderXAxis = () => {
    let ticks = [];
    const xStart = -props.world_width / 2;
    const numXAxisTicks = props.world_width / distanceBetweenTicks + 1;
    const xStep = distanceBetweenTicks;
    for (let i = 0; i < numXAxisTicks; i++) {
      ticks.push(
        <g
          class="tick"
          opacity="1"
          transform={`translate(${scaleFactor * distanceBetweenTicks * i},0)`}
        >
          <line
            stroke="currentColor"
            y2={scaleFactor * props.world_height}
            strokeWidth="5"
          ></line>
        </g>
      );
    }
    return (
      <g
        class="x-axis"
        fill="none"
        font-size="40"
        font-family="sans-serif"
        text-anchor="middle"
      >
        {ticks}
      </g>
    );
  }

  const renderYAxis = () => {
    let ticks = [];
    const yStart = props.world_height / 2;
    const numYAxisTicks = props.world_height / distanceBetweenTicks + 1;
    const yStep = distanceBetweenTicks;
    for (let i = 0; i < numYAxisTicks; i++) {
      ticks.push(
        <g
          class="tick"
          opacity="1"
          transform={`translate(0,${scaleFactor * distanceBetweenTicks * i})`}
        >
          <line
            stroke="currentColor"
            x2={scaleFactor * props.world_width}
            strokeWidth="5"
          ></line>
        </g>
      );
    }
    return (
      <g
        class="y-axis"
        fill="none"
        font-size="40"
        font-family="sans-serif"
        text-anchor="start"
      >
        {ticks}
      </g>
    );
  }

  const renderGrid = () => {
    return (
      <React.Fragment>
        <rect
          width={scaleFactor * props.world_width}
          height={scaleFactor * props.world_height}
          fill="white"
        ></rect>

        {renderXAxis()}

        {renderYAxis()}
      </React.Fragment>
    );
  }

  //returns an array of x and y deltas from center point to vertices of a regular polygon with a given numberOfSides and a given sideLength
  const generateRegularPolygonDeltas = (numberOfSides, sideLength) => {
    const individualVertexAngle = 2 * Math.PI / numberOfSides;
    const radius = Math.sqrt(sideLength * sideLength / (2 - 2 * Math.cos(individualVertexAngle)));
    const initialAngleOffset = -Math.PI / 2 + (numberOfSides % 2 == 0 ? individualVertexAngle / 2 : 0);
    const deltas = [];
    for (let i = 0; i < numberOfSides; i++) {
      deltas.push({ x: radius * Math.cos(initialAngleOffset + i * individualVertexAngle), y: radius * Math.sin(initialAngleOffset + i * individualVertexAngle) })
    }
    return deltas;
  }

  const getDeltasFromVerticesXAndY = (x, y, vertices) => {
    return vertices.map((vertex) => ({ x: vertex['x'] - x, y: vertex['y'] - y }));
  }

  const getPolygonInfoFromVertices = (vertices) => {
    const center = vertices.reduce(
      (previousValue, currentValue) => ({ x: previousValue['x'] + currentValue['x'] / vertices.length, y: previousValue['y'] + currentValue['y'] / vertices.length }),
      { x: 0, y: 0 }
    );
    return { x: center['x'], y: center['y'], deltas: this.getDeltasFromVerticesXAndY(center['x'], center['y'], vertices) };
  }


  const renderObjects = () => {
    let objects = [];
    for (const detection of detections) {
      switch (
      detection["type"] ? String(detection["type"].toLowerCase().trim()) : ""
      ) {
        case "minibot":
          objects.push(renderBot(detection));
          break;
        case "virtual_object":
        case "physical_object":
          objects.push(renderShapeGroup(detection));
          break;
        default:
          objects.push(renderUnknown(detection));
          break;
      }
    }
    return <React.Fragment>{objects}</React.Fragment>;
  }

  const renderBot = (detection) => {
    detection["shape"] = "cube";
    detection["width"] = botWidth;
    detection["length"] = botLength;
    detection["height"] = botHeight;
    detection["color"] = detection["color"] || "red";
    return renderShapeGroup(detection, "./static/img/bot-dot.png");
  }

  const renderUnknown = (detection) => {
    const x_pos = parseFloat(detection["x"]);
    const y_pos = parseFloat(detection["y"]);
    const orientation_pos = parseFloat(detection["orientation"]);
    return renderShapeGroup(
      detection["shape"] ? detection : {
        shape: "circle",
        x: x_pos,
        y: y_pos,
        orientation: orientation_pos,
        width: 2 * unknownMeasure,
        height: 2 * unknownMeasure,
        color: unknownColor,
      },
      "./static/img/unknown-dot.png"
    );
  }

  const renderShapeGroup = (detection, image_path = null) => {
    const x_pos = parseFloat(detection["x"]);
    const y_pos = parseFloat(detection["y"]);
    const x = scaleFactor * (props.world_width / 2 + x_pos);
    const y = scaleFactor * (props.world_height / 2 - y_pos);
    const orientation_pos = parseFloat(detection["orientation"]);
    return (
      <g className="popup" onClick={() => {
        alert(`${detection["name"] ? detection["name"] : ""}: (${Math.round(
          x_pos
        )},${Math.round(y_pos)}) ${Math.round(orientation_pos)}°, id: ${detection['id']}`)
      }}>
        <title>{`${detection["name"] ? detection["name"] : ""}: (${Math.round(
          x_pos
        )},${Math.round(y_pos)}) ${Math.round(orientation_pos)}°, id: ${detection['id']}`}</title>
        {renderShape(orientation_adjusted_detection, image_path)}
      </g >
    );
  }

  const renderShape = (detection, image_path) => {
    const x_pos = parseFloat(detection["x"]);
    const y_pos = parseFloat(detection["y"]);
    const x = scaleFactor * (props.world_width / 2 + x_pos);
    const y = scaleFactor * (props.world_height / 2 - y_pos);
    const orientation_pos = parseFloat(detection["orientation"]);
    const width = detection["width"] ? detection["width"] : unknownMeasure;
    const height = detection["length"] ? detection["length"] : unknownMeasure;
    const radius = detection["radius"] ? detection["radius"] : unknownMeasure;
    const radiusY = detection["radiusY"] ? detection["radiusY"] : unknownMeasure;
    const deltas_to_vertices = detection["deltas_to_vertices"] ? detection["deltas_to_vertices"] : [];
    const vertices = deltas_to_vertices.map(
      (currentValue) => new Vector(currentValue['x'], currentValue['y'])
    );
    const text_vertices = deltas_to_vertices.reduce(
      (previousValue, currentValue) => `${previousValue} ${x + scaleFactor * currentValue['x']},${y + scaleFactor * currentValue['y']}`,
      ""
    );

    const average_deltas_to_vertices_radius = deltas_to_vertices.reduce(
      (previousValue, currentValue) => previousValue + Math.sqrt(currentValue['x'] * currentValue['x'] + currentValue['y'] * currentValue['y']) / deltas_to_vertices.length,
      0
    );
    switch (
    detection["shape"] ? String(detection["shape"].toLowerCase().trim()) : ""
    ) {
      case "cube":
      case "rectangular-prism":
      case "rectangular-prism":
      case "square":
      case "rectangle":
        return (
          <React.Fragment>
            <rect
              x={x - (scaleFactor * width) / 2}
              y={y - (scaleFactor * height) / 2}
              transform={`rotate(${orientation_pos}, ${x}, ${y})`}
              width={scaleFactor * width}
              height={scaleFactor * height}
              fill={detection["color"]}
            ></rect>
            {image_path && renderShape(
              {
                x: x_pos,
                y: y_pos,
                orientation: orientation_pos,
                width: width,
                length: height,
                color: detection["color"],
                shape: "image",
              },
              image_path
            )}
          </React.Fragment>
        );
      case "sphere":
      case "cylinder":
      case "circle":
        return (
          <React.Fragment>
            <circle
              cx={x}
              cy={y}
              r={scaleFactor * radius}
              fill={detection["color"] ? detection["color"] : unknownMeasure}
              transform={`rotate(${orientation_pos}, ${x}, ${y})`}
            ></circle>
            {image_path && renderShape(
              {
                x: x_pos,
                y: y_pos,
                orientation: orientation_pos,
                width: 2 * radius,
                length: 2 * radius,
                color: detection["color"],
                shape: "image",
              },
              image_path
            )}
          </React.Fragment>
        );
      case "oval":
      case "ellipse":
      case "ellipsoid":
        return (
          <React.Fragment>
            <ellipse
              cx={x}
              cy={y}
              rx={scaleFactor * radius}
              ry={scaleFactor * radiusY}
              fill={detection["color"] ? detection["color"] : unknownMeasure}
              transform={`rotate(${orientation_pos}, ${x}, ${y})`}
            ></ellipse>
            {image_path && renderShape(
              {
                x: x_pos,
                y: y_pos,
                orientation: orientation_pos,
                width: 2 * radius,
                length: 2 * radiusY,
                color: detection["color"],
                shape: "image",
              },
              image_path
            )}
          </React.Fragment>
        );
      case "image":
        return (
          <image
            x={x - (scaleFactor * width) / 2}
            y={y - (scaleFactor * height) / 2}
            width={scaleFactor * width}
            height={scaleFactor * height}
            fill={
              scaleFactor *
              (detection["color"] ? detection["color"] : unknownMeasure)
            }
            href={image_path || "./static/img/unknown-dot.png"}
            transform={`rotate(${orientation_pos}, ${x}, ${y})`}
          ></image>
        );
      case "regular_polygon":
      case "polygon":
      default:
        return (
          <React.Fragment>
            <polygon
              points={text_vertices}
              fill={detection["color"] ? detection["color"] : unknownMeasure}
              transform={`rotate(${orientation_pos}, ${x}, ${y})`}
            ></polygon>
            {image_path && renderShape(
              {
                x: x_pos,
                y: y_pos,
                orientation: orientation_pos,
                width: average_deltas_to_vertices_radius,
                length: average_deltas_to_vertices_radius,
                color: detection["color"],
                shape: "image",
              },
              image_path
            )}
          </React.Fragment>
        );
    }
  }

  const renderSVG = () => {
    return (
      <svg
        width={props.view_width}
        height={props.view_height}
        fill="white"
        viewBox={`0 0 ${scaleFactor * props.world_width + 2 * widthPadding
          } ${scaleFactor * props.world_height + 2 * heightPadding}`}
      >
        <g transform={`translate(${widthPadding},${heightPadding})`}>
          {renderGrid()}
          {renderObjects()}
        </g>
      </svg>
    );
  }





  const getVisionData = () => {
    // allows you to call global attributes in axios
    // example of adding object mapping to base station

    axios
      .get("/vision", { params: { virtual_room_id: virtualRoomId } })
      .then(
        function (response) {
          setDetections(response.data ? response.data : []);
        }.bind(this)
      )
      .catch(function (error) {
        // console.log(error);
      });



  }

  const checkCollisions = () => {
    if (detections && detections.length > 1) {
      // logIfShapesCollide(detections);
    }
  }

  const toggleVisionDisplay = () => {
    if (displayOn) {
      clearInterval(displayIntervalId);
      clearInterval(collisionIntervalId);
      setDisplayOn(false);
      setDetections([]);
    }
    // if we make this interval too small (like 10ms), the backend can't
    // process the requests fast enough and the server gets overloaded
    // and cannot handle any more requests.  If you want to poll faster,
    // then we need to make the backend be able to handle requests
    // concurrently, or we need to use WebSockets which will hopefully
    // allow for faster communication
    else {
      setDisplayIntervalId(setInterval(getVisionData, 100));
      setCollisionIntervalId(setInterval(checkCollisions, 100));
      setDisplayOn(true);
    }
  }


  if (displayOn) {
    return (
    <React.Fragment>
      {!props.defaultEnabled && <button
        onClick={toggleVisionDisplay}
        className="btn btn-secondary ml-1"
      >
        {displayOn ? "Stop Displaying Field" : "Display Field"}
      </button>}

      <br />
      <TransformWrapper
        initialScale={1}
        initialPositionX={0}
        initialPositionY={0}
      >
        {({ zoomIn, zoomOut, resetTransform }) => (
          <React.Fragment>
            <TransformComponent>{renderSVG()}</TransformComponent>
          </React.Fragment>
        )}
      </TransformWrapper>
    </React.Fragment>
    );}
   
  else { return (<div></div>); }
}

export default withCookies(GridView);