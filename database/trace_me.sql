-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 06, 2024 at 02:18 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `trace_me`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `camera` varchar(20) NOT NULL,
  `location` varchar(40) NOT NULL,
  `fine` int(11) NOT NULL,
  `video_file` varchar(50) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`, `camera`, `location`, `fine`, `video_file`, `mobile`, `email`) VALUES
('admin', 'admin', 'Cam1.2', 'west road, bus stand, Salem', 500, 'v1.mp4', 9894442716, 'san@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `camera_info`
--

CREATE TABLE `camera_info` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `camera_id` varchar(20) NOT NULL,
  `location` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `camera_info`
--

INSERT INTO `camera_info` (`id`, `uname`, `camera_id`, `location`) VALUES
(1, 'T1', 'Cam1.1', 'SS Road'),
(2, 'T2', 'C113', 'Chatram, Trichy');

-- --------------------------------------------------------

--
-- Table structure for table `detection`
--

CREATE TABLE `detection` (
  `id` int(11) NOT NULL,
  `vno` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `fine` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `camera` varchar(100) NOT NULL,
  `location` varchar(40) NOT NULL,
  `tc` varchar(20) NOT NULL,
  `date_time` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `alert_type` int(11) NOT NULL,
  `message` varchar(50) NOT NULL,
  `pdate` varchar(20) NOT NULL,
  `pay_st` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `detection`
--

INSERT INTO `detection` (`id`, `vno`, `name`, `fine`, `status`, `camera`, `location`, `tc`, `date_time`, `alert_type`, `message`, `pdate`, `pay_st`) VALUES
(1, 'TN21AT0480', 'Anurag', 500, 0, '', 'Karur Bye Pass', 'T1', '2024-04-06 07:43:11', 1, '', '2024-04-08', 0),
(2, 'TN21AT0480', 'Anurag', 500, 0, '', 'Karur bye pass', 'T1', '2024-04-06 15:47:39', 1, '', '2024-04-06', 0),
(3, 'TN21AT0480', 'Anurag', 500, 0, '', 'Karur bye pass', 'T1', '2024-04-06 15:55:03', 1, '', '2024-04-06', 0),
(4, 'TN21AT0480', 'Anurag', 0, 0, '', 'Karur bye pass', 'T1', '2024-04-06 17:32:40', 2, 'Towing may be enforced', '', 0),
(5, 'TN21AT0480', 'Anurag', 500, 0, '', 'Karur bye pass', 'T1', '2024-04-06 17:33:15', 1, '', '2024-04-06', 0),
(6, 'TN21AT0480', 'Anurag', 100, 0, '', 'Karur bye pass', 'T1', '2024-04-06 17:33:46', 1, '', '2024-04-07', 0),
(7, 'TN21AT0480', 'Anurag', 500, 0, '', 'Karur bye pass', 'T1', '2024-04-06 17:39:21', 1, '', '2024-04-07', 0),
(8, 'TN21AT0480', 'Anurag', 500, 0, '', 'Karur bye pass', 'T1', '2024-04-06 18:22:12', 1, '', '2024-04-07', 0),
(9, 'TN21AT0480', 'Anurag', 500, 0, '', 'Karur bye pass', 'T1', '2024-04-06 19:44:50', 1, '', '2024-04-07', 1);

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `vno` varchar(20) NOT NULL,
  `filename` varchar(20) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `dob` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `address` varchar(50) NOT NULL,
  `register_date` varchar(20) NOT NULL,
  `vtype` varchar(30) NOT NULL,
  `vmodel` varchar(100) NOT NULL,
  `vcolor` varchar(20) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `vname` varchar(30) NOT NULL,
  `driving` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `name`, `vno`, `filename`, `gender`, `dob`, `mobile`, `email`, `address`, `register_date`, `vtype`, `vmodel`, `vcolor`, `uname`, `pass`, `vname`, `driving`) VALUES
(1, 'Anurag', 'TN21AT0480', 'C33.jpg', 'Male', '1976-02-09', 9894442716, 'anurag@gmail.com', '45,DF Nagar, Chennai', '2020-09-05', '4 Wheeler', 'Creta 2020', 'Red', 'V1', '2470', 'Hyundai', 'D3d1.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `tm_rto`
--

CREATE TABLE `tm_rto` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `location` varchar(50) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tm_rto`
--

INSERT INTO `tm_rto` (`id`, `name`, `mobile`, `email`, `location`, `uname`, `pass`) VALUES
(1, 'Kumar', 7352125562, 'kumar@gmail.com', 'Chennai', 'R1', '4219');

-- --------------------------------------------------------

--
-- Table structure for table `traffic_control`
--

CREATE TABLE `traffic_control` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `area` varchar(30) NOT NULL,
  `city` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `traffic_control`
--

INSERT INTO `traffic_control` (`id`, `name`, `mobile`, `email`, `area`, `city`, `uname`, `pass`) VALUES
(1, 'Ganesh', 9856748488, 'ganesh@gmail.com', 'RR Nagar', 'Trichy', 'T1', '1234');
