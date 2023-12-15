import React, { useState } from "react";
import { FileUploader } from "react-drag-drop-files";
import classes from "./ImagesDragger.module.scss";
// NOTE: we can't use react-beautiful-dnd, bevause it's not typed. Use @hello-pangea/dnd instead! 
// https://github.com/atlassian/react-beautiful-dnd/issues/2401#issuecomment-1215229217
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd'; 
import classNames from "classnames";

const fileTypes = ["JPG", "PNG", 'AVIF', 'WEBP'];
interface ImgSquareProps {
    orderNumber: number;
    imgFile: File;
}

const ImagesDragger = () => {
    const [imageSquares, setImageSquares] = useState<ImgSquareProps[]>();

    const handleChange = (filesList: any) => {
        // take first 3 images    
        filesList = Object.values(filesList).slice(0, 3) // convert dict to list
        const filesDict = filesList.map((fileObj: File, i: number) => {return {orderNumber: i, imgFile: fileObj}})
        setImageSquares(filesDict);
        console.log('filesDict', filesDict)
    };

    function handleOnDragEnd(result: any) {
        console.log('result', result)
        if (!result.destination) return;

        const items = Array.from(imageSquares!);
        const [reorderedItem] = items.splice(result.source.index, 1);
        items.splice(result.destination.index, 0, reorderedItem);

        setImageSquares(items);
    }

    return (
        <>
        {!imageSquares?
            <FileUploader 
                handleChange={handleChange} 
                name="file" 
                types={fileTypes} 
                multiple={true}
                required
            >
                <div className={classes.box}>
                    Upload up to 3 images here
                </div>
            </FileUploader>
            :
            <DragDropContext onDragEnd={handleOnDragEnd}>
                <Droppable 
                    droppableId="imagesSquares"
                    direction = 'horizontal'
                >
                    {(provided: any) => (
                        <div 
                            className={classNames(classes.imagesSquares, 'imagesSquares')}
                            {...provided.droppableProps} 
                            ref={provided.innerRef}
                        >
                            {imageSquares.map((sq, index) => {
                                return (
                                    <Draggable 
                                        key={sq.orderNumber.toString()}
                                        draggableId={sq.orderNumber.toString()} 
                                        // index={sq.orderNumber} 
                                        index={index}
                                    >
                                        {(provided: any) => (
                                            <div 
                                                key={sq.orderNumber} 
                                                className={classes.imgSquare}
                                                ref={provided.innerRef} 
                                                {...provided.draggableProps} 
                                                {...provided.dragHandleProps}
                                            >
                                                <img src={URL.createObjectURL(sq.imgFile)} />
                                            </div>
                                        )}
                                    </Draggable>
                                )
                            })}
                            {provided.placeholder}
                        </div>
                    )}
                </Droppable>
            </DragDropContext>
        }
        </>
    );
}

export default ImagesDragger
