import Dialog from "@material-ui/core/Dialog";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";

export default function AboutDialog(props) {
    return (
        <Dialog {...props}>
            <DialogTitle id="about-dialog-title">
                {"About WA COVID Vaccines"}
            </DialogTitle>
            <DialogContent>
                <DialogContentText id="about-dialog-description">
                    <p>
                        The {" "}
                        <a
                            href="https://www.doh.wa.gov/YouandYourFamily/Immunization/VaccineLocations"
                            target="_blank"
                            rel="noreferrer"
                        >
                             WA DOH
                        </a>
                        &nbsp;has done a great job pulling together information on the
                        various vaccine providers in the state,
                        but it's still pretty difficult to see which locations have
                        availability, if any. I wrote this website to try to help out!
                    </p>
                    <p>
                        My name is {" "}
                        <a
                            href="http://www.josephmin.com"
                            target="_blank"
                            rel="noreferrer"
                        >
                            Joe
                        </a>
                        &nbsp;and I'm doing my best to write enough code to scrape
                        every source listed on the WA DOH site to display here.
                        But, I work full time, so I can only do so much, so if
                        you're interested in helping out, feel free to {" "}
                        <a href="mailto:joe@josephmin.com">
                            shoot me an email
                        </a>
                        &nbsp;and let's talk!
                    </p>
                </DialogContentText>
            </DialogContent>
        </Dialog>
    );
}
