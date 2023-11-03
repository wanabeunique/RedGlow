import styles from './Proflie.module.sass';
import { Link } from 'react-router-dom';
import ChangePhoto from '@/components/SVG/ChangePhoto';
import { useState } from 'react';
import AvatarEditor from 'react-avatar-editor';
import getProfile from '../../api/getProfile';
import { useRef } from 'react';
import { useEffect } from 'react';
import { Progress } from '@/components/ui/progress';
import getUserFriends from '@/api/getUserFriends';
import defaultBg from '@/assets/profile-bg.png';
import defaultAvatar from '@/assets/profile-photo.png';
import Friend from '@/components/Friends/Friend/Friend';
import { useDropzone } from 'react-dropzone';
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

import { IOwnProfile } from '@/interfaces/IOwnProfile';
import changePhoto from '@/api/changePhoto';
import base64toFile from '@/functions/base64toFile';
import { useAppSelector } from '@/hooks';
import { IDate } from '@/functions/parseDate';
import parseDate from '@/functions/parseDate';
import changeBgPhoto from '@/api/changeBgPhoto';
import getUserBackground from '@/api/getUserBackground';

export default function OwnProfile() {
  const userPhoto = useAppSelector((store) => store.userReducer.photo);
  const [userBackground, setUserBackground] = useState<string>();

  const [friendsCurrentPage, setFriendsCurrentPage] = useState<number>(1);
  const [selectedPhoto, setSelectedPhoto] = useState<any>('');
  const [selectedBgPhoto, setSelectedBgPhoto] = useState<any>('');
  const [parsedDate, setParsedDate] = useState<IDate>();
  const [user, setUser] = useState<IOwnProfile>();
  const [decency, setDecency] = useState<number>(0);
  const [reports, setReports] = useState<number>(0);
  const [friendsData, setFriendsData] = useState<any>([]);

  const {
    acceptedFiles: acceptedBgFiles,
    getRootProps: getRootBgProps,
    getInputProps: getInputBgProps,
  } = useDropzone({
    accept: 'image/*',
    onDrop: (acceptedFiles) => {
      setSelectedBgPhoto(acceptedFiles[0]);
    },
  });

  const { acceptedFiles, getRootProps, getInputProps } = useDropzone({
    accept: 'image/*',
    onDrop: (acceptedFiles) => {
      setSelectedPhoto(acceptedFiles[0]);
    },
  });

  const EditorRef = useRef(null);
  const EditorBgRef = useRef(null);

  useEffect(() => {
    const getUser = async () => {
      const userData = await getProfile();
      setUser(userData);
      const parsedDate = parseDate(userData.date_joined);
      setParsedDate(parsedDate);
      const userBackground = await getUserBackground(userData.username);
      setUserBackground(userBackground);
    };
    getUser();
  }, []);

  useEffect(() => {
    if (user) {
      setDecency(Math.ceil(user.decency / 100));
      setReports(user.reports);
    }
  }, [user]);

  useEffect(() => {
    if (user) {
      const HandleFriends = async () => {
        const friendsDataValue: Array<string> = await getUserFriends(
          user.username,
          friendsCurrentPage,
        );
        setFriendsData(friendsDataValue);
      };
      HandleFriends();
    }
  }, [user]);

  async function changeAvatar() {
    setSelectedPhoto(null);
    const canvas = EditorRef.current.getImageScaledToCanvas();
    const image = canvas.toDataURL();
    changePhoto(base64toFile(image, 'avatar.png'));
  }

  async function changeBg() {
    setSelectedBgPhoto(null);
    const canvas = EditorBgRef.current.getImageScaledToCanvas();
    const image = canvas.toDataURL();
    console.log(image);
    changeBgPhoto(base64toFile(image, 'bg.png'));
  }

  return user ? (
    <div className={`${styles.profile}`}>
      <div className={styles.profile__top}>
        <img
          src={userBackground || defaultBg}
          className={styles.profile__top_bg}
        />
        <AlertDialog>
          <AlertDialogTrigger className={`${styles.profile__top_bg_trigger} ${styles.profile__top_change}`}>
            <ChangePhoto />
          </AlertDialogTrigger>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle></AlertDialogTitle>
              <AlertDialogDescription>
                {!selectedBgPhoto && (
                  <div
                    {...getRootBgProps({ className: 'dropzone' })}
                    className={styles.dropzone}
                  >
                    <input {...getInputBgProps()} />
                    <p className={styles.dropzone__text}>
                      Перетащите cюда сюда или нажмите, чтобы выбрать файлы
                    </p>
                  </div>
                )}
                {selectedBgPhoto && (
                  <AvatarEditor
                    ref={EditorBgRef}
                    width={1080}
                    height={250}
                    border={50}
                    scale={1.2}
                    className={styles.edit}
                    image={selectedBgPhoto}
                  />
                )}
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel
                onClick={() => {
                  setSelectedBgPhoto(null);
                }}
              >
                Отмена
              </AlertDialogCancel>
              <AlertDialogAction onClick={() => changeBg()}>
                Выберите изображение
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
        <div className="container">
          <div className={`${styles.profile__top_wrapper}`}>
            <div className={styles.profile__top_avatar}>
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
                              Перетащите cюда сюда или нажмите, чтобы выбрать
                              файлы
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
              <img
                className={styles.user__photo}
                src={userPhoto || defaultAvatar}
              />
            </div>
            <div className={styles.profile__top_text}>
              <p className={`${styles.profile__top_nickname} title`}>
                {user ? user.username : null}
              </p>
              <p className={`${styles.profile__top_registratedTime} text`}>
                На сайте с {parsedDate?.day} {parsedDate?.month}{' '}
                {parsedDate?.year}
              </p>
            </div>
          </div>
        </div>
      </div>
      <div
        className={`container ${styles.profile__content} grid grid-cols-6 gap-10`}
      >
        <div className={`${styles.profile__left} col-span-4 `}>
          <p className="mt-10">История игр</p>
          <div className="flex w-full gap-10">
            <div className={`${styles.profile__decency} mt-10 w-1/2`}>
              <p>Порядочность: {user?.decency} из 1000 </p>
              <Progress value={decency} />
            </div>
            <div className={`${styles.profile__decency} mt-10 w-1/2`}>
              <p>
                На вас было оставлено {reports} жалоб, осталось еще{' '}
                {100 - reports} до временной блокировки{' '}
              </p>
              <Progress value={reports} />
            </div>
          </div>
        </div>
        <div className={styles.profile__right}>
          <Link to="/settings">
            <p>Настройки</p>
          </Link>
          <p className={`mt-10 ${styles.friends__title}`}>Список друзей:</p>
          {friendsData.length > 0 ? (
            <div className={`${styles.friends__items} mt-5`}>
              {friendsData.map((friend: any) => (
                <Friend
                  username={friend.username}
                  type="current"
                  avatar={friend.photo}
                />
              ))}
            </div>
          ) : (
            <p
              className={styles.friends__text}
            >{`У вас пока что нет ни одного друга, но не стоит расстраиваться...`}</p>
          )}
        </div>
      </div>
    </div>
  ) : null;
}
