import { Separator } from "@/components/ui/separator";
import { Input } from "@/components/ui/input";
import styles from "./Proflie.module.sass";
import { useState, useEffect } from "react";
import { IOwnProfile } from "@/interfaces/IOwnProfile";
import getProfile from "@/api/getProfile";
import removeBodyClasses from "@/functions/civilization5/removeBodyClasses";
import { Button } from "@/components/ui/button";
import changePassword from "@/api/changePassword";
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
} from "@/components/ui/alert-dialog"
  
export default function ProfileSettings(){
  const [user, setUser] = useState<IOwnProfile>();
  const [currentPassword, setCurrentPassword] = useState<any>("");
  const [newPassword, setNewPassword] = useState<any>("");

   async function HandeChangePassword() {
      await changePassword(currentPassword, newPassword);
      setCurrentPassword("");
      setNewPassword("");
    }
 useEffect(() => {
      const getUser = async () => {
        const userData = await getProfile();
        setUser(userData);
      };
      getUser(); 
    }, []);
  return(
  <div className="container">
    <div className={`mt-10 ${styles.profile__item}`}>
      <div className={`${styles.profile__row}`}>
        <p>Steam аккаунт</p>
        {user?.steamIdExists === true ? (
          <p>Привязан</p>
        ) : (
          <a href="https://steamcommunity.com/openid/login?openid.ns=http://specs.openid.net/auth/2.0&openid.mode=checkid_setup&openid.claimed_id=http://specs.openid.net/auth/2.0/identifier_select&openid.identity=http://specs.openid.net/auth/2.0/identifier_select&openid.return_to=https://localhost/steam&openid.realm=https://localhost">
            Привязать аккаунт
          </a>
        )}
      </div>
    </div>
    <Separator />
    <div className={`${styles.profile__item}`}>
      <p>Ваш пароль: </p>
      <div className={styles.profile__row}>
        <p>******</p>
        <AlertDialog>
          <AlertDialogTrigger>Сменить пароль</AlertDialogTrigger>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>
                Вы точно хотите помнять пароль?
              </AlertDialogTitle>
              <AlertDialogDescription>
                <p>Введите текущий пароль</p>
                <Input
                  value={currentPassword}
                  onChange={(event) => {
                    setCurrentPassword(event.target.value);
                    console.log(event.target.value);
                  }}
                  className="mt-2"
                  type="password"
                />
                <p className="mt-2">Введите новый пароль</p>
                <Input
                  className="mt-2"
                  type="password"
                  value={newPassword}
                  onChange={(event) => {
                    setNewPassword(event.target.value);
                    console.log(event.target.value);
                  }}
                />
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Отмена</AlertDialogCancel>
              <AlertDialogAction onClick={() => HandeChangePassword()}>
                Сменить пароль
              </AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      </div>
    </div>
    <Separator />
    <div className={styles.profile__item}>
      <p>Электронная почта: </p>
      <div className={styles.profile__row}>
        <p>{user?.email}</p>
        <AlertDialog>
          <AlertDialogTrigger>Сменить почту</AlertDialogTrigger>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>
                Are you absolutely sure?
              </AlertDialogTitle>
              <AlertDialogDescription>
                This action cannot be undone. This will permanently
                delete your account and remove your data from our
                servers.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction>Continue</AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      </div>
    </div>
    <Separator />
    <div className={styles.profile__item}>
      <p>Номер телефона: </p>
      <div className={styles.profile__row}>
        <p>{user?.phoneNumber}</p>
        <AlertDialog>
          <AlertDialogTrigger>Сменить номер</AlertDialogTrigger>
          <AlertDialogContent>
            <AlertDialogHeader>
              <AlertDialogTitle>
                Are you absolutely sure?
              </AlertDialogTitle>
              <AlertDialogDescription>
                This action cannot be undone. This will permanently
                delete your account and remove your data from our
                servers.
              </AlertDialogDescription>
            </AlertDialogHeader>
            <AlertDialogFooter>
              <AlertDialogCancel>Cancel</AlertDialogCancel>
              <AlertDialogAction>Continue</AlertDialogAction>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialog>
      </div>
    </div>
    <div className="flex flex-col gap-2">
      Выбор темы:
      <div className=" grid grid-cols-4 gap-3">
        <Button
          onClick={() => {
            removeBodyClasses();
            document.querySelector("html")?.classList.add("theme-blue");
          }}
        >
          Синяя тема
        </Button>
        <Button
          onClick={() => {
            removeBodyClasses();
            document.querySelector("html")?.classList.add("theme-red");
          }}
        >
          Красная тема
        </Button>
        <Button
          onClick={() => {
            removeBodyClasses();
            document
              .querySelector("html")
              ?.classList.add("theme-orange");
          }}
        >
          Оранжевая тема
        </Button>
        <Button
          onClick={() => {
            removeBodyClasses();
            document.querySelector("html")?.classList.add("theme-zink");
          }}
        >
          Серая тема
        </Button>
        <Button
          onClick={() => {
            removeBodyClasses();
            document
              .querySelector("html")
              ?.classList.add("theme-violet");
          }}
        >
          Фиолетовая тема
        </Button>
      </div>
    </div>
  </div>
  )
}
