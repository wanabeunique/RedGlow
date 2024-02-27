import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';
import styles from '@/pages/Profile/Proflie.module.sass';
import ChangePhoto from '../SVG/ChangePhoto';
import { useRef, useState } from 'react';
import userService from '@/service/user.service';
import { useDropzone } from 'react-dropzone';
import AvatarEditor from 'react-avatar-editor';
import base64toFile from '@/functions/base64toFile';

export default function changeProfilePhoto() {
  const EditorRef = useRef(null);

  async function changeAvatar() {
    setSelectedPhoto(null);
    const canvas = EditorRef.current.getImageScaledToCanvas();
    const image = canvas.toDataURL();
    userService.setUserPhoto(base64toFile(image, 'avatar.png'));
  }

  const { acceptedFiles, getRootProps, getInputProps } = useDropzone({
    accept: 'image/*',
    onDrop: (acceptedFiles) => {
      setSelectedPhoto(acceptedFiles[0]);
    },
  });
  
  

  const [selectedPhoto, setSelectedPhoto] = useState('');

  return (
    <label className={styles.profile__top_change}>
      <AlertDialog>
        <AlertDialogTrigger className={styles.profile__top_trigger}>
          <ChangePhoto />
        </AlertDialogTrigger>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle></AlertDialogTitle>
            <AlertDialogDescription>
              {!selectedPhoto && (
                <div
                  {...getRootProps({ className: 'dropzone' })}
                  className={styles.dropzone}
                >
                  <input {...getInputProps()} />
                  <p className={styles.dropzone__text}>
                    Перетащите cюда сюда или нажмите, чтобы выбрать файлы
                  </p>
                </div>
              )}
              {selectedPhoto && (
                <AvatarEditor
                  ref={EditorRef}
                  width={250}
                  height={250}
                  border={50}
                  scale={1.2}
                  className={styles.edit}
                  image={selectedPhoto}
                />
              )}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel
              onClick={() => {
                setSelectedPhoto(null);
              }}
            >
              Отмена
            </AlertDialogCancel>
            <AlertDialogAction onClick={() => changeAvatar()}>
              Выберите изображение
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </label>
  );
}
